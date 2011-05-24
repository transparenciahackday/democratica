$(function() {
    
    /* STATEMENT SHARING BUTTONS */
    
    if ($('body').hasClass('dar')) {
        var $statementTools = $('<div id="statement-tools" style="display: block">Olá<img id="share_link" src="/static/images/link.png" class="tip" title="Share a link to this statement"><img id="share_twitter" src="/static/images/twitter.png" class="tip" alt="Twitter" title="Share on Twitter"><img id="share_facebook" src="/static/images/facebook.png" class="tip" title="Share on Facebook"></div>');
        $statementTools.bind('mouseenter', function () {$statementTools.show();})
            .bind('mouseleave', function () {$statementTools.hide();})
            .find('.tip').tooltip({delay: 100, showURL: false});
        $paginated.after($statementTools);
        var $currentStatement;
        function currentStatementURL() {
            return 'https://demo.cratica.org' + $currentStatement.attr('data-url');
        }
        function currentStatementDescription() {
            var descr = $currentStatement.find('.pol_name').html();
            if (!descr) {
                descr = $('.pol_name').html();
            }
            var topic = $currentStatement.find('.statement_topic').html();
            if (topic) {
                descr += ' on ' + topic;
            }
            return descr;
        }
        $('.intervention').live('mouseenter', function() {
            $currentStatement = $(this);
            var offset = $currentStatement.position();
            $statementTools.css({'top': offset.top, 'left': offset.left + ($currentStatement.width() - 66)}).show();
        }).live('mouseleave', function() {$statementTools.hide();});
        $('#share_link').click(function() {
            if (!$currentStatement.find('.share_link').length) {
                var linkbox = $('<input type="text">').val(currentStatementURL()).click(function() {
                    if (this.createTextRange) {
                        // This is for IE and Opera.
                        range = this.createTextRange();
                        range.moveEnd('character', this.value.length);
                        range.select();
                    } else if (this.setSelectionRange) {
                        // This is for Mozilla and WebKit.
                        this.setSelectionRange(0, this.value.length);
                    }});
                $currentStatement.find('.focus').prepend($('<p class="share_link">Copy this link: </p>').append(linkbox));
            }
        });
        $('#share_facebook').click(function() {
            openparlShareWindow('http://facebook.com/sharer.php?'
                + $.param({'u': currentStatementURL(),
                't': currentStatementDescription()}));
        });
        $('#share_twitter').click(function() {
            openparlShareWindow('http://twitter.com/share?'
                + $.param({'url': currentStatementURL(),
                'via': 'openparlca',
                'related': 'openparlca:openparliament.ca',
                'text': currentStatementDescription()
                }));
            // window.open(currentStatementURL() + 'twitter/');
        });
    }
});