"use strict"

$(function() {
  var $help = $('.help');
  var textarea = $('form textarea')[0];
  var speechSupported = 'speechSynthesis' in window;

  function say(msg) {
    var msg;

    if (!speechSupported) return;

    msg = new SpeechSynthesisUtterance(msg);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
  }

  function showHelp(msg) {
    $help.text(msg);
    say(msg);
  }

  function getLineNumber(index) {
    var substr = textarea.value.substring(0, index);

    return substr.split('\n').length;
  }

  function getSyntaxHelp(html, index) {
    var result = Slowparse.HTML(document, html, {
      disallowActiveAttributes: true
    });
    var node, tagInfo;

    function isInside(tagInfo) {
      if (!tagInfo) return false;
      return index > tagInfo.start && index < tagInfo.end;
    }

    function isInContent(parseInfo) {
      if (!(parseInfo.openTag && parseInfo.closeTag)) return false;
      return index >= parseInfo.openTag.end &&
             index <= parseInfo.closeTag.start;
    }

    function descend(parent) {
      var tagName;
      var descendants;

      for (var i = 0; i < parent.childNodes.length; i++) {
        node = parent.childNodes[i];
        tagName = node.nodeName;
        if (node.parseInfo) {
          if (isInside(node.parseInfo.openTag)) {
            if (node.parseInfo.closeTag) {
              return "inside an opening " + tagName + " tag";
            } else {
              return "inside a " + tagName + " tag";
            }
          } else if (isInside(node.parseInfo.closeTag)) {
            return "inside a closing " + tagName + " tag";
          } else if (isInContent(node.parseInfo)) {
            descendants = descend(node);
            return descendants + " inside a " + tagName + " element";
          }
        }
      }

      return '';
    }

    if (!result.document) {
      return '';
    }

    return descend(result.document);
  }

  if (speechSupported) {
    // This browser supports the Web Speech API, which is going to be
    // a lot more reliable than the screen reader's intepretation of
    // the ARIA spec, so we'll enable text-to-speech and disable ARIA for
    // our help system.
    $help
      .removeAttr('role')
      .removeAttr('aria-live')
      .attr('aria-hidden', 'true');
  }

  $(document).keydown(function(e) {
    var index, help, syntaxHelp;

    if (e.key == 'h' && e.ctrlKey) {
      e.preventDefault();

      index = textarea.selectionStart;
      syntaxHelp = getSyntaxHelp(textarea.value, index);
      help = 'Cursor is on line ' + getLineNumber(index);

      if (syntaxHelp) {
        help += ', ' + syntaxHelp;
      }

      help += '.';

      showHelp(help);
    }
  });
});
