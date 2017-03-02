$(function() {
  var tags       = new Map(),
      people     = [],
      tokens     = new Map(),
      totalWords = 0,
      maxFreq    = 0;
  window.tags = tags;
  window.tokens = tokens;

  var width  = 900,
      height = 600;

  var fill = d3.scaleOrdinal(d3.schemeCategory20b);

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
        var tokenFreq = freqs[token];
        tokens.set(token, tokenFreq + tokens.get(token));
        totalWords += tokenFreq;
        maxFreq = Math.max(maxFreq, tokenFreq);
      }
    }
  }

  function generateWords(size) {
    var words = [];

    tokens.forEach(function(freq, token) {
      words.push({
        text: token,
        value: ~~(24 * freq / maxFreq)
      });
    });

    words.sort(function(a, b) { return b.value - a.value; });
    words = words.slice(0, size);

    return words;
  }

  function draw(layout, words) {
    var size = layout.size();
    console.log('draw', words);

    d3.select('#sky').append('svg')
        .attr('width',  size[0])
        .attr('height', size[1])
      .append('g')
        .attr('transform', 'translate(' + size[0] / 2 + ',' + size[1] / 2 + ')')
      .selectAll('text')
        .data(words)
      .enter().append('text')
        .style('font-size', function(d) { return d.value + 'px'; })
        .style('font-family', 'Impact')
        .style('fill', function(d, i) { return fill(i); })
        .attr('text-anchor', 'middle')
        .attr('transform', function(d) {
          console.log(d.x, d.y);
          return 'translate(' + [d.x, d.y] + ') rotate(' + d.rotate + ')';
        })
        .text(function(d) { return d.text; })
      ;
  }

  d3.json(
    'data/people-data.json',
    function(data) {
      var layout;

      people = data;
      window.people = people;

      data.forEach(function(person) {
        if (person.tags != null) {
          indexTags(person);
        }
        accumulateTokenCounts(person.text);
      });

      layout = d3.layout.cloud()
                    .size([width, height])
                    .padding(5)
                    .words(generateWords(100))
                    // .rotate(function() { return ~~(Math.random() * 2) * 90; })
                    .font('Impact')
                    .fontSize(function(d) { return d.size; })
                    .on('end', function(words) { return draw(layout, words); })
                    ;
      layout.start();

      // TODO: set up cloud from totals
      // TODO: set up tag selection widget
      // TODO: tag selection change transition event handlers
    });
});
