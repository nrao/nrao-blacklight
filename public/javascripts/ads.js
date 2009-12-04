(function() {

  //var ads = document.location.toString().replace(/\/[^\/]*(\?|#|$)/, '/ads-json.php/');
  var ads = 'https://safe.nrao.edu/php/library/ads-json.php/';

  // Only one request at a time unless this is made dynamic
  var callback_name = 'ads_callback';

  var $ = jQuery;

  window.get_ads_links = function get_ads_links(bibcode, cb) {
    var url = ads + encodeURIComponent(bibcode) + '?callback=' + callback_name;

    window[callback_name] = function cb_wrapper(data) {
      // Catch errors here, or firebug misses them.
      try {
    cb(data);
      } catch (e) {
    if ('console' in window)
      console.log('FAIL: ', e);
      // In case anyone else cares.
      throw e;
      }
    };

    jQuery.getScript(url);
  };

  window.create_ads_links = function create_ads_links(bibcode, el) {
    get_ads_links(bibcode, function got_ads_links(data) {
      for (var key in data[0].links) {
        if (key != "EJOURNAL") {
    if (data[0].links[key] instanceof Object) {
      var linkel = $('<div class="ads-link"><a/></div>')
        .addClass('ads-link-'+key)
        .attr({
        title: data[0].links[key].name
        })
        .children('a')
          .text(key)
          .attr({
          href: data[0].links[key].url
          })
        .end()
        .appendTo(el);
    }
        }
      }
    });
  }

})();
