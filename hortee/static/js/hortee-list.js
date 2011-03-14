$(function(){

var oldSync = Backbone.sync;
 
    Backbone.sync = function(method, model, success, error){
        var newSuccess = function(resp, status, xhr){
            if(xhr.statusText === "CREATED"){
                var location = xhr.getResponseHeader('Location');
                return $.ajax({
                    url: location,
                    success: success
                });
            }
            return success(resp);
        };
        return oldSync(method, model, newSuccess, error);
    };

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
    });
 
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
            'click p': 'remove'
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
        toggle: function() {
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
            this.actions.create({
                actor: this.model.attributes.resource_uri,
                text: this.$('input').val()
            });
            this.$('input').val('');
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
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        change: function() {
            console.log('foo');
        }
    });
    
    window.PlotContainerView = Backbone.View.extend({
        el: $('#plots'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'toggle');
            
            window.plots = new Plots()
            plots.bind('add', this.addOne);
            plots.bind('refresh', this.addAll);
            plots.fetch();
            
            $('h2').click(this.toggle);
        },
        toggle: function() {
            this.el.toggle();
        },
        addAll: function() {
            plots.each(this.addOne);
        },
        addOne: function(plot) {
            var view = new PlotView({ model: plot });
            this.$('ul').append(view.render().el);
        }
    });
    
    window.AppView = Backbone.View.extend({
        el: $('#app'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll');
            
            window.user = new User({
                'username': USER_NAME
            }).fetch();
            
            this.plotContainerView = new PlotContainerView();
            
            window.actors = new Actors();
            actors.bind('add', this.addOne);
            actors.bind('refresh', this.addAll);
            actors.fetch();
        },
        addAll: function() {
            actors.each(this.addOne);
        },
        addOne: function(actor) {
            var view = new ActorView({ model: actor });
            this.$('#actors').append(view.render().el);
        }
    });    

    window.app = new AppView();
});
