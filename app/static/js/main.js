
//TODO: Get new data every 20 seconds
function getAccountBalance(currency_class){
$(currency_class).each(function() {
            var elem = $(this);
            $.post(window.location.pathname + "check-balance",{
            currency: elem.find( "select option:selected",this ).text(),
        },
            function (data) {
               elem.find('.balance').text("Your Wallet Balance: " + data);
               elem.find('.balance').css('display','inline');

            }
        );
    });
}