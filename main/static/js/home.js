$(function(){
    $('#update').click(function () {
        $('#q').val('update " " set " "  where " "') ;
    });
    $('#select').click(function () {
        $('#q').val('select " " from " " where " "') ;
    });

    $('#insert').click(function () {
        $('#q').val('insert into " " " " values " "') ;
    });

    $('#delete').click(function () {
        $('#q').val('delete from " " where " "') ;
    });
});     



