$( document ).ready(function() {
    var hold_selected;
    var guess_selected;
    function build_twitter_url(move_id, text) {
        var options = {
            url: 'http://spoof.albertmanya.com/m/' + move_id,
            screen_name: $( '#id_adversary' ).val(),
            button_hashtag: 'SpoofTwitterEd',
            text: text
            count: 'none',
            size: 'large'
        };
        var params = $.param(options);
        return 'https://twitter.com/share?' + params;
    }
    $('#id_initiator').keyup( function() {
        var $this = $(this);
        if( $this.val().length > 0 ) {
            $('#initiator_hold').show('slow');
        }
    });
    $('.btn-hold').click( function() {
        var selected = $(this).text();
        hold_selected = parseInt(selected);
        for(var i=0; i<hold_selected; i++) {
            $('#btn-guess-' + i.toString()).attr('disabled', '');
        }
        $('#id_initiator').attr('disabled', '');
        $('#btn-restart').show('slow');
        $('#initiator_adversary').show('slow');
        $('.btn-hold').each(function() {
            var $el = $(this);
            if($el.text() == selected) {
                $el.addClass('btn-success');
            } else {
                $el.removeClass('btn-success');
            }
        });
    });
    $('#id_adversary').keyup( function() {
        var $this = $(this);
        if( $this.val().length > 0 ) {
            $('.btn-hold').attr('disabled', '');
            $('#initiator_guess').show('slow');
        }
    });
    $('.btn-guess').click(function() {
        var selected = $(this).text();
        guess_selected = parseInt(selected);
        $('#msgsend').text('Click the Tweet button to send the challenge to @' + $('#id_adversary').val() + ':');
        $('#tweet_btn').show('slow');
        $('#id_adversary').attr('disabled', '');
        $.ajax({
            type: "POST",
            url: "/mkmove",
            data: {
                'initiator': $('#id_initiator').val(),
                'adversary': $('#id_adversary').val(),
                'initiator_hold': hold_selected,
                'initiator_guess': guess_selected
            }
        }).done(function(msg) {
            $('.twitter-share-button').attr('href', build_twitter_url(msg.moveid, msg.text));
            /* This line taken from twitter-button docu */
            !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="https://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
        });
        $('.btn-guess').each(function() {
            var $el = $(this);
            if($el.text() == selected) {
                $el.addClass('btn-success');
            }
        });
        $('.btn-guess').attr('disabled', '');
    });
    $('#btn-restart').click(function() {
        $('#tweet_btn').hide('slow', function() {
            $('#initiator_guess').hide('slow', function() {
                $('#initiator_adversary').hide('slow', function() {
                    $('#initiator_hold').hide('slow');
                    $('#btn-restart').hide('slow');
                    $('.btn-guess').removeAttr('disabled')
                                   .val('');
                    $('.btn-guess').each(function() {
                        $(this).removeClass('btn-success');
                    });
                    $('#id_adversary').removeAttr('disabled')
                                      .val('');
                    $('.btn-hold').removeAttr('disabled')
                    $('.btn-hold').each(function() {
                        $(this).removeClass('btn-success');
                    });
                    $('.btn-group button').removeClass('active');
                    $('#id_initiator').removeAttr('disabled')
                                      .val('');
                });
            });
        });
    });
});


