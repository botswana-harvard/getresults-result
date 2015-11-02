/*!
 * Getresults_result
 */


/*!
 * Getresults_result release funcs
 */

function func_enable_save_buttons() {
	$( "#button-id-save" ).prop( "disabled", false );
	$( "#button-id-savenext" ).prop( "disabled", false );	
	$( "#button-id-next" ).prop( "disabled", true );	
	$( "#button-id-previous" ).prop( "disabled", true );	
}

function func_disable_save_buttons() {
	$( "#button-id-save" ).prop( "disabled", true );
	$( "#button-id-savenext" ).prop( "disabled", true );	
	$( "#button-id-next" ).prop( "disabled", false );	
	$( "#button-id-previous" ).prop( "disabled", false );	
}

function func_release() {
	$( "#id_status" ).prop( "value", "release" );
	func_enable_save_buttons();
	$( "#button-id-release" ).removeClass( "btn-default" ).addClass( "btn-success" );
	$( "#button-id-review" ).removeClass( "btn-info" ).addClass( "btn-default" );
}

function func_review() {
	$( "#id_status" ).prop( "value", "review" );
	func_enable_save_buttons();	
	$( "#button-id-release" ).removeClass( "btn-success" ).addClass( "btn-default" );
	$( "#button-id-review" ).removeClass( "btn-default" ).addClass( "btn-info" );
}

function func_cancel(form_id) {
	$( "#id_status" ).prop( "value", "" );
	$( "#id_navigation" ).prop( "value", "cancel" )
	$( "#"+form_id ).submit();
}

function func_previous(form_id) {
	$( "#id_status" ).prop( "value", "" );
	$( "#id_navigation" ).prop( "value", "previous" )
	$( "#"+form_id ).submit();
}

function func_next(form_id) {
	$( "#id_status" ).prop( "value", "" );
	$( "#id_navigation" ).prop( "value", "next" )
	$( "#"+form_id ).submit();
}

function func_save(form_id) {
	$( "#id_navigation" ).prop( "value", "" )
	$( "#"+form_id ).submit();
}

function func_savenext(form_id) {
	$( "#id_navigation" ).prop( "value", "savenext" )
	$( "#"+form_id ).submit();
}


/*!
 * Getresults_result validate funcs
 */

function func_set_validation_status(){
	var arr_status = [];
	$( '[id^=id_validation_status_text]' ).each( function( i ) {
		func_validation_status( $( this ).html(), i );
	});
}

function func_validation_status( status,n ) {
	validation_status=$( "#id_validation_status_text_" + n);
	validation_status.html(status);
	validation_status.removeClass("bg-danger text-danger text-warning text-info text-success");
    if( status=='accept' ){ validation_status.addClass( 'text-success' ); }
    if( status=='repeat' ){ validation_status.addClass( 'text-info' ); }
    if( status=='cancel' ){ validation_status.addClass( 'text-danger' ); }
    if( status=='ignore' ){ validation_status.addClass( 'text-warning' ); }
    $( "#id_form-"+n+"-status" ).prop( "value",status );
    $( '#accept_'+n ).removeClass( 'text-success' ).addClass( 'text-muted' );
    $( '#repeat_'+n ).removeClass( 'text-info' ).addClass( 'text-muted' );
    $( '#cancel_'+n ).removeClass( 'text-danger' ).addClass( 'text-muted' );
    $( '#ignore_'+n ).removeClass( 'text-warning' ).addClass( 'text-muted' );
    selected_icon=$( '#'+status+'_'+n );
    if( status=='accept' ){ selected_icon.addClass( 'text-success' ); }
    if( status=='repeat' ){ selected_icon.addClass( 'text-info' ); }
    if( status=='cancel' ){ selected_icon.addClass( 'text-danger' ); }
    if( status=='ignore' ){ selected_icon.addClass( 'text-warning' ); }
}

function func_reset_validation_all_buttons() {
	$( "#button-id-accept_all" ).removeClass( "btn-success" ).addClass( "btn-default" )
	$( "#button-id-repeat_all" ).removeClass( "btn-info" ).addClass( "btn-default" )
	$( "#button-id-cancel_all" ).removeClass( "btn-danger" ).addClass( "btn-default" )
	$( "#button-id-ignore_all" ).removeClass( "btn-warning" ).addClass( "btn-default" )
}

function func_update_validation_icons(status){
	var n = -1;
	$( "#div-id-validation_status span" ).each( function() {
		if ( $( this ).attr( "id" ).indexOf( status ) == 0 ) {
			n += 1;
			func_validation_status( status, n );
		}
	});
}

function func_reset_validation_icons(){
	var n = -1;
	var arr_status = ['accept', 'repeat', 'cancel', 'ignore']
	$.each( arr_status, function( index, status ){
		n = -1
		$( "#div-id-validation_status span" ).each( function() {
			if ( $( this ).attr( "id" ).indexOf( status ) == 0 ) {
				n += 1;
				func_validation_status( 'pending', n );
			}
		});
	});
}

function func_accept_all() {
	func_enable_save_buttons();
	func_reset_validation_all_buttons();
	$( "#button-id-accept_all" ).removeClass( "btn-default" ).addClass( "btn-success" );
	func_update_validation_icons( 'accept' );
}

function func_repeat_all() {
	func_enable_save_buttons();
	func_reset_validation_all_buttons();
	$( "#button-id-repeat_all" ).removeClass( "btn-default" ).addClass( "btn-info" )
	func_update_validation_icons( 'repeat' );
}

function func_cancel_all() {
	func_enable_save_buttons();
	func_reset_validation_all_buttons();
	$( "#button-id-cancel_all" ).removeClass( "btn-default" ).addClass( "btn-danger" )
	func_update_validation_icons( 'cancel' );
}

function func_ignore_all() {
	func_enable_save_buttons();
	func_reset_validation_all_buttons();
	$( "#button-id-ignore_all" ).removeClass( "btn-default" ).addClass( "btn-warning" )
	func_update_validation_icons( 'ignore' );
}

function func_reset_all() {
	location.reload();
}
