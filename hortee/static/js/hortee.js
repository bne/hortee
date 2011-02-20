$(function(){

    window.Plot = Backbone.Model.extend({
        url: function() {
            return this.get('resource_uri') || this.collection.url;
        }
    });
    
    window.Plots = Backbone.Collection.extend({
        model: Plot,
        url: API_ENDPOINT + 'plot/',
        parse: function(data){
            return data.objects;
        }         
    });
    
    window.PlotView = Backbone.View.extend({
        tagName: 'li',
        className: 'plots',
        template: _.template($('#plot-template').html()),
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    window.App = Backbone.View.extend({
        el: $('#app'),
        
        initialize: function() {
            _.bindAll(this, 'addOne', 'addAll', 'render');
            this.plots = new Plots();
            this.plots.bind('add', this.addOne);
            this.plots.bind('refresh', this.addAll);
            this.plots.bind('all', this.render);
            this.plots.fetch();
        },
        
        addAll: function(){
          this.plots.each(this.addOne);
        },

        addOne: function(plot){
          var view = new PlotView({ model: plot });
          this.$('#plots').append(view.render().el);
        },
    });
    
    window.app = new App();
});
