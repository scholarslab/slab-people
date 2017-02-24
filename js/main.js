$(function() {
  var tags   = new Map(),
      people = [],
      tokens = new Map();
  window.tags = tags;
  window.tokens = tokens;

  function expandFrequencies(freqs) {
    var items = [];
    freqs.forEach(function(v, k) {
      for (var i=0; i<v; i++) {
        items.push(k);
      }
    });
    return items;
  }

  function indexTags(person) {
    person.tags.forEach(function(tag) {
      if (!tags.has(tag)) {
        tags.set(tag, []);
      }
      tags.get(tag).push(person);
    });
  }

  function accumulateTokenCounts(freqs) {
    for (var token in freqs) {
      if (freqs.hasOwnProperty(token)) {
        if (!tokens.has(token)) {
          tokens.set(token, 0);
        }
        tokens.set(token, freqs[token] + tokens.get(token));
      }
    }
  }

  d3.json(
    'data/people-data.json',
    function(data) {
      people = data;
      window.people = people;

      data.forEach(function(person) {
        if (person.tags != null) {
          indexTags(person);
        }
        accumulateTokenCounts(person.text);
      });

      // TODO: set up cloud from totals
      // TODO: set up tag selection widget
      // TODO: tag selection change transition event handlers
    });
});
