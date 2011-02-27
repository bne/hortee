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

    window.Actor = Backbone.Model.extend({
        initialize: function() {
            this.events = new window.Events;
            this.events.url = API_DISCO['event'].list_endpoint + '?actor=' + this.id;
            this.events.actor = this;
        },
        url: function() {
            return this.get('resource_uri');
        }        
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
            //'tap h3 .event-add': 'toggleEventAdd',
            'click h3 .event-add': 'toggleEventAdd'
        },
        initialize: function() {
            this.model.view = this;
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        toggleEventAdd: function(ev) {
            ev.cancelBubble = true;
            var form = $(this.el).find('form.event');
            if(form.css('display') == 'none') {
                form.show();
            }
            else {
                form.hide();
            }
        }
    });
    
    window.App = Backbone.View.extend({
        el: $('#app'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'render');
            this.actors = new Actors();
            this.actors.bind('add', this.addOne);
            this.actors.bind('refresh', this.addAll);
            this.actors.bind('all', this.render);
            this.actors.fetch();
        },
        
        addAll: function(){
          this.actors.each(this.addOne);
        },

        addOne: function(actor){
          var view = new ActorView({ model: actor });
          this.$('#actors').append(view.render().el);
        },
    });    

    window.app = new App();  
});
