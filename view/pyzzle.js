$( document ).ready(function() {
    setupBoard(4);
});

function setupBoard(board_dimension) {
    var board = $( ".board" );

    createTiles(board, board_dimension);

    $( '.tile-occupied' ).click(function( event ) {
        console.log($(this))

        if($(this).isAfter('#tile_empty')) {
            $(this).insertBefore($(this).prev('#tile_empty'));
        } else if($(this).isBefore('#tile_empty')) {
            $(this).insertAfter($('#tile_empty'));
        }
    });
}

function createTiles(board, board_dimension) {
    var board_tiles = Math.pow(board_dimension, 2)
    var current_row = createRow(board);

    // add empty tile to first row
    createTile(current_row, "tile_empty", "(empty)", "tile-base");

    // add occupied tiles
    for (i = 1; i <= board_tiles - 1; i++) {
        if (i % board_dimension == 0) {
            current_row = createRow(board);
        }

        createTile(current_row, null, i, "tile-base tile-occupied");
    }

}

function createTile(row, id, content, classes_str) {
    var elem = "<td"
    if (id != null) {
        elem += " id='" + id + "'";
    }
    elem += " class='" + classes_str + "'><p>" + content + "</p></td>";

    row.append(elem);
}

function createRow(board) {
    var row = $("<tr>");
    board.append(row);

    return row;
}

$.fn.isAfter = function(sel) {
  return this.prev(sel).length !== 0;
}

$.fn.isBefore= function(sel) {
  return this.next(sel).length !== 0;
}