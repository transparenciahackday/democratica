var Dashboard = function(data_endpoint, selector_key, update_interval, num_points) {
  this.dashboard_data = {};
  this.max_data_point = 0;
  this.data_endpoint = data_endpoint;
  this.selector_key = selector_key;
  this.num_points = num_points || 60; /* default to showing 60 points */
  
  var self = this;
  this.fetch_every(update_interval * 1000, function(data) {
    self.load_data(data);
    self.plot_data();
  });
};

Dashboard.prototype.make_id = function(id) {
  return 'id-' + id;
}

Dashboard.prototype.load_data = function(data) {
  for (var i = 0; i < data.length; i++) {
    var panel_data = data[i],
        data_points = panel_data.data,
        panel_id = panel_data.panel_id,
        point_id = panel_data.point_id;
    
    if (!this.dashboard_data[panel_id])
      this.dashboard_data[panel_id] = {};
    
    var dd = this.dashboard_data[panel_id];
    
    for (var label in data_points) {
      dd[label] = dd[label] || {};
      dd[label][this.make_id(point_id)] = [point_id, data_points[label]];
    }
    
    if (point_id > this.max_data_point)
      this.max_data_point = point_id;
    
    this.dashboard_data[panel_id] = dd;
  }
};

Dashboard.prototype.fetch_data = function(callback) {
  $.getJSON(this.data_endpoint + '?max_id=' + this.max_data_point, callback);
};

Dashboard.prototype.fetch_every = function(timeout, callback) {
  var self = this;
  this.fetch_data(function(data) {
    callback(data);
    setTimeout(function(){ self.fetch_every(timeout, callback) }, timeout);
  });
};

Dashboard.prototype.plot_data = function() {
  var dd = this.dashboard_data;
  
  for (var panel_id in dd) {
    var panel_data = [];
    
    for (var label in dd[panel_id]) {
      var label_data = [],
          normalized = [];
      
      for (var point_id in dd[panel_id][label]) {
        label_data.push(dd[panel_id][label][point_id]);
      }
      
      label_data.sort(function(l, r) {
        return l[0] - r[0];
      });
      
      var data_length = label_data.length;
      
      /* only display the most recent `num_points` items */
      for (var i = (data_length - this.num_points); i < data_length; i++) {
        if (label_data[i]) {
          normalized.push([i, label_data[i][1]]);
        } else {
          normalized.push([i, 0]);
        }
      }
    
      /* remove ids we no longer care about */
      for (var i = 0; i < data_length; i++) {
        var id_to_remove = label_data[i][0];
        delete dd[panel_id][label][id_to_remove];
      }
      
      panel_data.push({
        'label': label,
        'data': normalized
      });
    }
    $.plot($('#dashboard-' + this.selector_key + '-' + panel_id), panel_data, {
      xaxis: {ticks: []},
      legend: {
        show: true,
        noColumns: 4,
        container: $('#legend-' + this.selector_key + '-' + panel_id)
      }
    });
  }
};
