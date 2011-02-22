$(function(){

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
    
    window.ActorView = Backbone.View.extend({
        tagName: 'li',
        className: 'actor',
        template: _.template($('#actor-template').html()),
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
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
