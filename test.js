var google = require('google');
var Q = require('q');
var fs = require('fs');

google.resultsPerPage = 100;
var nextCounter = 0;
var items = {};

var explode = function(term, placement) {
  var d = Q.defer();

  var query = function(thisNext) {
    console.log(thisNext, term);
    google(term, function(err, next, links){
      if (err) console.error(err);
      if (typeof items[term] == 'undefined') {
        items[term] = {
          placement: placement,
          links: []
        };
      }

      for (var i = 0; i < links.length; ++i) {
        items[term].links.push(links[i]);
      }

      if (thisNext < 100) {
        setTimeout(function() {
          query(thisNext + 1);
        }, 1000);
      } else {
        d.resolve();
      }
    });
  };

  query(0);
  return d.promise;
}

var writeItems = function(outputFilename) {
  fs.writeFile(outputFilename, JSON.stringify(items, null, 4), function(err) {
    if(err) {
      console.log(err);
    } else {
      console.log("JSON saved to " + outputFilename);
    }
  });
};

// var word = 'is exploding';
// var word = 'are exploding';
var word = 'exploded';
// var word = 'will explode';
// var word = 'has exploded';
// var word = 'are currently exploding';
// var word = 'is currently exploding';
// var word = 'has recently exploded';

explode('"' + word + '"', 'before').then(
  function() {
    var filename = '_' + word.split(' ').join("_") + ".json";
    writeItems(filename);
  }
);
