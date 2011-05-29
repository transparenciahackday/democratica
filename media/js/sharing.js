
/* openparliament custom javascript */
function openparlShareWindow(url) {
    var width = 550;
    var height = 450;
    var left = Math.round((screen.width / 2) - (width / 2));
    var top = 0;
    if (screen.height > height) {
        top = Math.round((screen.height / 2) - (height / 2));
    }
    window.open(url, "openparliament_share", "width=" + width +
       ",height=" + height + ",left=" + left, ",top=" + top +
       "personalbar=no,toolbar=no,scrollbars=yes,location=yes,resizable=yes");
}


$(function() {
    
    /* STATEMENT SHARING BUTTONS */
    
   // if ($('body').hasClass('dar')) {
        var $statementTools = $('<div id="statement-tools" style="display: block">Olá<img id="share_link" src="/media/img/adim.png" class="tip" title="Share a link to this statement"><img id="share_twitter" src="/media/img/adim.png" class="tip" alt="Twitter" title="Share on Twitter"><img id="share_facebook" src="/media/img/adim.png" class="tip" title="Share on Facebook"></div>');
        $statementTools.bind('mouseenter', function () {$statementTools.show();})
            .bind('mouseleave', function () {$statementTools.hide();})
            //.find('.tip').tooltip({delay: 100, showURL: false});
        // $paginated.after($statementTools);
        var $currentStatement;
        function currentStatementURL() {
            return 'https://demo.cratica.org/sessoes/intervencao/' + $currentStatement.attr('id');
        }
        function currentStatementDescription() {
            var descr = $currentStatement.find('.mp-name').html();
            if (!descr) {
                descr = $('.mp-name').html();
            }
            //var topic = $currentStatement.find('.statement_topic').html();
            //if (topic) {
            //    descr += ' on ' + topic;
            //}
            //return descr;
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
                'via': 'demo_cratica',
                'related': 'demo_cratica:demo.cratica.org',
                'text': currentStatementDescription()
                }));
            // window.open(currentStatementURL() + 'twitter/');
        });
    //}
});
