$( document ).ready(function() {
    var hold_selected;
    var guess_selected;
    function build_twitter_url() {
        var options = {
            url: 'http://spoof.albertmanya.com/',
            screen_name: $( '#id_adversary' ).val(),
            button_hashtag: 'SpoofTwitterEd',
            text: 'You have been challenged!',
            count: 'none',
            size: 'large'
        };
        var params = $.param(options);
        return 'https://twitter.com/share?' + params;
    }
    $('.btn-hold').click( function() {
        $('#adversary_guess').show('slow');
        var selected = $(this).text();
        hold_selected = parseInt(selected);
        for(var i=0; i<hold_selected; i++) {
            $('#btn-guess-' + i.toString()).attr('disabled', '');
        }
        for(var i=hold_selected; i<=6; i++) {
            $('#btn-guess-' + i.toString()).removeAttr('disabled');
        }
        $('.btn-hold').each(function() {
            var $el = $(this);
            if($el.text() == selected) {
                $el.addClass('btn-success');
            } else {
                $el.removeClass('btn-success');
            }
        });
    });
    $('.btn-guess').click(function() {
        $('#btn-restart').show('slow');
        $('#make_guess').show('slow');
        $('.btn-hold').attr('disabled', '');
        var selected = $(this).text();
        guess_selected = parseInt(selected);
        $('.btn-guess').each(function() {
            var $el = $(this);
            if($el.text() == selected) {
                $el.addClass('btn-success');
            }
        });
        $('.btn-guess').attr('disabled', '');
    });
    $('#btn-restart').click(function() {
        $('#make_guess').hide('slow', function() {
            $('#adversary_guess').hide('slow', function() {
                $('#btn-restart').hide('slow');
                $('.btn-guess').removeAttr('disabled')
                               .val('');
                $('.btn-guess').each(function() {
                    $(this).removeClass('btn-success');
                });
                $('.btn-hold').removeAttr('disabled')
                $('.btn-hold').each(function() {
                    $(this).removeClass('btn-success');
                });
                $('.btn-group button').removeClass('active');
            });
        });
    });
    $('#btn-challenge').click(function() {
        $('.btn-hold').attr('disabled', '');
        $('#btn-restart').hide('slow');
        $('#btn-challenge').attr('disabled', '');
        $.ajax({
            type: "POST",
            url: "/f/" + moveid,
            data: {
                'adversary_hold': hold_selected,
                'adversary_guess': guess_selected,
            }
        }).done(function(msg) {
            alert(msg)
        });
    });
});


