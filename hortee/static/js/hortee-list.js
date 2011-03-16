$(function(){

    window.Action = Backbone.Model.extend({
        url: function() {
            return this.get('resource_uri') || this.collection.url;
        }        
    });
    
    window.Actions = Backbone.Collection.extend({
        model: Action,
        url: API_DISCO['action'].list_endpoint,
        parse: function(data){
            return data.objects;
        }        
    });this.list
 
    window.Actor = Backbone.Model.extend({
        url: function() {
            return this.get('resource_uri') || this.collection.url;
        }
    });
    
    window.Actors = Backbone.Collection.extend({
        model: Actor,
        url: API_DISCO['actor'].list_endpoint,
        parse: function(data){
            return data.objects;
        }         
    });
    
    window.Plot = Backbone.Model.extend({
        url: function() {
            return this.get('resource_uri') || this.collection.url;
        }    
    });
    
    window.Plots = Backbone.Collection.extend({
        model: Plot,
        url: API_DISCO['plot'].list_endpoint,
        parse: function(data){
            return data.objects;
        }         
    });
        
    window.User = Backbone.Model.extend({
        initialize: function(o) {
            this.url = API_DISCO['user'].list_endpoint + o.username;
        }
    });
    
    /*
        Views
    */
    
    window.ActionView = Backbone.View.extend({
        tagName: 'li',
        className: 'action',
        template: _.template($('#action-template').html()),
        events: {
            'click .delete': 'remove'
        },
        initialize: function() {
            _.bindAll(this, 'render', 'remove');
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        remove: function() {
            this.model.destroy();
            $(this.el).remove();
        }
    });    
    
    window.ActorView = Backbone.View.extend({
        tagName: 'li',
        className: 'actor',
        template: _.template($('#actor-template').html()),
        events: {
            'click h3': 'toggle',
            'keypress input': 'createOnEnter'
        },
        initialize: function() {    
            _.bindAll(this, 'addOne', 'addAll', 'render', 'add', 'create');
            this.actions = new Actions;
            this.actions.url += '?actor=' + this.model.id;
            this.actions.bind('add', this.addOne);
            this.actions.bind('refresh', this.addAll);
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            this.list = this.$('ul.actions');
            this.list.hide();            
            return this;
        },        
        toggle: function(evt) {
            evt.stopPropagation();
            var show = (this.list.css('display')=='none');
            $('ul.actions').hide();
            if(show) {
                this.list.show();
                if(!this.actions.loaded) {
                    this.actions.fetch();
                    this.actions.loaded = true;
                }
            }
        },       
        addAll: function(){            
            this.actions.each(this.addOne);
            $('li.loading', this.list).remove();
        },
        addOne: function(action){
            var view = new ActionView({ model: action });
            $(view.render().el).insertAfter($('li:first', this.list));
        },
        createOnEnter: function(evt) {
            evt.stopPropagation();   
            if (evt.keyCode == 13) {
                this.create();
            }
        },
        create: function() {
            var text = this.$('input').val();
            if(text) {
                this.actions.create({
                    actor: this.model.attributes.resource_uri,
                    text: this.$('input').val()
                }, { 
                    success: function() { $('input').removeClass('loading'); }
                });
                this.$('input').addClass('loading');
                this.$('input').val('');
            }
        }
    });

    window.ActorsView = Backbone.View.extend({
        el: $('#actors'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll'); 
            window.actors = new Actors();
            actors.url += '?plot=' + window.currentPlot.id;
            actors.bind('add', this.addOne);
            actors.bind('refresh', this.addAll);
            actors.fetch();
        },
        addAll: function() {
            $('#actors').html('');
            actors.each(this.addOne);
        },
        addOne: function(actor) {
            var view = new ActorView({ model: actor });
            this.el.append(view.render().el);
        }
    });
    
    window.PlotView = Backbone.View.extend({
        tagName: 'li',
        className: 'plot',
        template: _.template($('#plot-template').html()),
        events: {
            'click': 'change'
        },
        initialize: function() {
            _.bindAll(this, 'change');
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        change: function(evt) {
            evt.stopPropagation();
            window.plotsView.hide();
            $('#actors').html('');
            $('#actors').append('<li class="loading"></li>');
            window.plotsView.setPlot(this.model);
        }
    });
    
    window.PlotsView = Backbone.View.extend({
        el: $('#plots'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'toggle', 'hide', 'setPlot');
            window.plots = new Plots()
            plots.bind('add', this.addOne);
            plots.bind('refresh', this.addAll);
            plots.fetch();
            
            $('h2').click(this.toggle);
            $(document).click(this.hide);
        },
        toggle: function(evt) {
            evt.stopPropagation();
            this.el.toggle();
        },
        hide: function() {
            this.el.hide();
        },
        setPlot: function(plot) {
            window.currentPlot = plot;
            $('h2').text(window.currentPlot.get('name'));
            this.actorsView = new ActorsView();
        },
        addAll: function() {
            plots.each(this.addOne);
            this.setPlot(plots.models[0]);
        },
        addOne: function(plot) {
            var view = new PlotView({ model: plot });
            this.$('ul').append(view.render().el);
        }
    });
    
    window.AppView = Backbone.View.extend({
        el: $('#app'),
        initialize: function() {            
            window.user = new User({
                'username': USER_NAME
            }).fetch();
            window.plotsView = new PlotsView();
        }
    });    

    window.app = new AppView();
});
