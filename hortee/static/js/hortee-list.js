$(function(){

    window.Action = Backbone.Model.extend({
        url: function() {
            return this.attributes.resource_uri || this.collection.url;
        }        
    });
    
    window.Actions = Backbone.Collection.extend({
        model: Action,
        url: API_DISCO['action'].list_endpoint,
        parse: function(data){
            return data.objects;
        }        
    });
    
    window.ActionView = Backbone.View.extend({
        tagName: 'li',
        className: 'action',        
        events: {
            'click p': 'remove'
        },
        template: _.template($('#action-template').html()),
        initialize: function() {
            this.model.view = this;
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        remove: function() {
            this.model.destroy();
        }
    });
 
    window.Actor = Backbone.Model.extend({
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'render');
            this.actions = new window.Actions;
            this.actions.url = API_DISCO['action'].list_endpoint + '?actor=' + this.id;
            this.actions.actor = this;
            this.actions.bind('add', this.addOne);
            this.actions.bind('refresh', this.addAll);
        },
        url: function() {
            return this.get('resource_uri');
        },        
        addAll: function(){
            this.actions.each(this.addOne);
        },
        addOne: function(action){
            
            var view = new ActionView({ model: action });
          $(this.view.el).find('ul.actions').append(view.render().el);
        },
    });
    
    window.Actors = Backbone.Collection.extend({
        model: Actor,
        url: API_DISCO['actor'].list_endpoint,
        parse: function(data){
            return data.objects;
        }         
    });
    
    window.ActorView = Backbone.View.extend({
        tagName: 'li',
        className: 'actor',
        template: _.template($('#actor-template').html()),
        events: {
            'click h3': 'toggleActions',
            'click span.btn.date': 'toggleCalendar',
            'click span.btn.add': 'addAction',
            'keypress input[type="text"]': 'addActionOnEnter'
        },
        initialize: function() {
            this.model.view = this;
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        toggleActions: function() {
            this.input = this.$('input[type="text"]');
            this.list = this.$('ul.actions');
            var show = (this.list.css('display') == 'none');
            $('ul.actions').hide();
            if(show) {
                this.list.show();
                if(!this.model.actions.loaded) {
                    this.model.actions.fetch();
                    this.model.actions.loaded = true;
                }
            }
        },
        toggleCalendar: function() {
            
        },
        addActionOnEnter: function(evt) {
            if (evt.keyCode != 13) return;
            evt.stopPropagation();
            this.addAction();
        },
        addAction: function() {    
            this.model.actions.create({
                actor: this.model.attributes.resource_uri,
                text: this.input.val()
            });
        }
    });
    
    window.AppView = Backbone.View.extend({
        el: $('#app'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'render');
            this.actors = new Actors();
            this.actors.bind('add', this.addOne);
            this.actors.bind('refresh', this.addAll);
            this.actors.fetch();
        },        
        addAll: function(){
          this.actors.each(this.addOne);
        },
        addOne: function(actor){
          var view = new ActorView({ model: actor });
          $('#actors').append(view.render().el);
        },
    });    

    window.app = new AppView();  
});
