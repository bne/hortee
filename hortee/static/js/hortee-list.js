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
            return this.attributes.resource_uri || this.collection.url;
        },
        initialize: function(){
            this.setupAssociations({
                    'actions': Actions
            });
        },
        setupAssociations:function(assoc){
            for ( var key in assoc ) {
                this[ key ] = new assoc[key]( this.get( key ),{ memberOf: this } );
                this.bind( 'change:' + key , _.bind( this.setAssociated, this, key ) );
            }
        },
        setAssociated: function(name, self, val){
            this[name].refresh(val);
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
        },
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        remove: function() {
            this.model.destroy();
            console.log(this.model.collection);
            $(this.el).remove();
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
            this.$('input').val('');
        }
    });
    
    window.AppView = Backbone.View.extend({
        el: $('#app'),
        events: {
            'click #addActor': 'create'
        },
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'render');
            Actors.bind('add', this.addOne);
            Actors.bind('refresh', this.addAll);
            Actors.bind('all', this.render);
            Actors.fetch();
        },        
        addAll: function() {
            window.Actors.each(this.addOne);
        },
        addOne: function(actor) {
            var view = new ActorView({ model: actor });
            this.$('#actors').append(view.render().el);
        },
        create: function() {
            Actors.create({
                plot: '/api/v1/plot/2/',
                name: 'Foo'
            });
        }
    });    

    window.app = new AppView();
});
