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

  function getLineNumber() {
    var index = textarea.selectionStart;
    var substr = textarea.value.substring(0, index);

    return substr.split('\n').length;
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
    if (e.key == 'h' && e.ctrlKey) {
      e.preventDefault();
      showHelp('Cursor is on line ' + getLineNumber() + '.');
    }
  });
});
