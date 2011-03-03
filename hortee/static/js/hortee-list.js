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
 
    window.Actor = Backbone.Model.extend({
        url: function() {
            return this.get('resource_uri');
        }
    });
    
    window.ActorList = Backbone.Collection.extend({
        model: Actor,
        url: API_DISCO['actor'].list_endpoint,
        parse: function(data){
            return data.objects;
        }         
    });
      
    window.Actors = new ActorList;
    
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
            this.model.bind('change', this.render);
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        remove: function() {
            this.model.destroy();
        }
    });    
    
    window.ActorView = Backbone.View.extend({
        tagName: 'li',
        className: 'actor',
        template: _.template($('#actor-template').html()),
        events: {
            'click h3': 'toggle',
            'keypress input[type="text"]': 'createOnEnter'
        },
        initialize: function() {    
            _.bindAll(this, 'addOne', 'addAll', 'render', 'add', 'create');
            this.actions = new Actions;
            this.actions.url += '?actor=' + this.model.id;
            this.actions.bind('add', this.addOne);
            this.actions.bind('refresh', this.addAll);
            this.actions.bind('create', this.addOne);
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
            this.list.append(view.render().el);
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
        }
    });
    
    window.AppView = Backbone.View.extend({
        el: $('#app'),
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll');
            Actors.bind('add', this.addOne);
            Actors.bind('refresh', this.addAll);
            Actors.fetch();
        },        
        addAll: function() {
            window.Actors.each(this.addOne);
        },
        addOne: function(actor) {
            var view = new ActorView({ model: actor });
            this.$('#actors').append(view.render().el);
        },
    });    

    window.app = new AppView();  
});
