$( document ).ready(function() {
    $( ".board" ).append( "<div id='tile_empty' class='tile-base'><p>(empty)</p></div>" );

    for(i=1; i<=15; i++){
        $( ".board" ).append( "<div class='tile-base tile-occupied'><p>" + i + "</p></div>" );
    }

    $( '.tile-occupied' ).click(function( event ) {
        console.log(event)
        console.log($(this))

        if($(this).isAfter('#tile_empty')) {
            $(this).insertBefore($(this).prev('#tile_empty'));
        } else if($(this).isBefore('#tile_empty')) {
            $(this).insertAfter($('#tile_empty'));
        }
    });


});

$.fn.isAfter = function(sel){
  return this.prev(sel).length !== 0;
}
$.fn.isBefore= function(sel){
  return this.next(sel).length !== 0;
}