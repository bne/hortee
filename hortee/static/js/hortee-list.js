$(function(){

    window.Event = Backbone.Model.extend({
        url: function() {
            return this.get('resource_uri');
        }        
    });
    
    window.Events = Backbone.Collection.extend({
        model: Event,
        parse: function(data){
            return data.objects;
        }        
    });
    
    window.EventView = Backbone.View.extend({
        tagName: 'li',
        className: 'event',
        template: _.template($('#event-template').html()),
        initialize: function() {
            this.model.view = this;
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        }
    });
 
    window.Actor = Backbone.Model.extend({
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'render');
            this.events = new window.Events;
            this.events.url = API_DISCO['event'].list_endpoint + '?actor=' + this.id;
            this.events.actor = this;
            this.events.bind('add', this.addOne);
            this.events.bind('refresh', this.addAll);
        },
        url: function() {
            return this.get('resource_uri');
        },        
        addAll: function(){
          this.events.each(this.addOne);
        },
        addOne: function(event){
          var view = new EventView({ model: event });
          $(this.view.el).find('ul.events').append(view.render().el);
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
            'click h3': 'toggleEvents'
        },
        initialize: function() {
            this.model.view = this;
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        toggleEvents: function(ev) {
            var event_list = $(this.el).find('ul.events');
            var show = (event_list.css('display') == 'none');
            $('ul.events').hide();
            if(show) {
                event_list.show();
                if(!this.model.events.loaded) {
                    this.model.events.fetch();
                    this.model.events.loaded = true;
                }
            }
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
