mf = {}

/// UTILITIES /////////////////////////////////////////////////////////////////////////////////

mf.templateEngine = function (templateId, args) {
	args = args || {};
	var template = $('#'+templateId).html();
	//console.log(templateId);
	for (arg in args) {
		var str = '[[' + arg + ']]'
		template = template.split(str).join(args[arg]);
	}
	return template;
}


/// EVENTS /////////////////////////////////////////////////////////////////////////////////////

mf.appendEvents = function() {
	mf.appendPostEvents();
	mf.appendCommentEvents();
}

mf.appendCommentEvents = function() {
	$('.new-comment-form').unbind();
	$('.new-comment-form').submit(function(e) {
		var postId = $(this).attr('data-post-id');
		//alert(postId);
		var data = $("#new-comment-form-"+postId).serialize();		// post_id, uid, body
		var url = "/microfeed/posts/comments/new";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var args = json;
			var result = mf.templateEngine('comment-template', args);
			$('#comments-'+json.postId).append(result);
			$("#new-comment-form-"+json.postId+' textarea[name=body]').val('');
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$('.edit-comment-btn').unbind();
	$('.edit-comment-btn').click(function(e) {
		var commentId = $(this).attr('data-comment-id');
		$('#comment-'+commentId).hide();
		$('#edit-comment-'+commentId).show();
		e.preventDefault();
	});
	
	$('.delete-comment-btn').unbind();
	$('.delete-comment-btn').click(function(e) {
		var commentId = $(this).attr('data-comment-id');
		$('#delete-comment-id').val(commentId);
		$('#delete-comment-modal').modal('show');
		e.preventDefault();
	});
	
	$('.cancel-edit-comment').unbind();
	$('.cancel-edit-comment').click(function() {
		var commentId = $(this).attr('data-comment-id');
		$('#edit-comment-'+commentId).hide();
		$('#comment-'+commentId).show();
	});
	
	$(".edit-comment-form").unbind();
	$(".edit-comment-form").submit(function(e) {
		var commentId = $(this).attr('data-comment-id');
		var data = $("#edit-comment-form-"+commentId).serialize();		// post_id, body
		var url = "/microfeed/posts/comments/edit";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var commentId = json.commentId;
			$('#comment-body-'+commentId).html(json.body);
			$('#edit-comment-'+commentId).hide();
			$('#comment-'+commentId).show();
			mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$("#delete-comment-form").unbind();
	$("#delete-comment-form").submit(function(e) {
		var data = $('#delete-comment-form').serialize();		// post_id, body
		var url = "/microfeed/posts/comments/delete";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var commentId = json.commentId;
			$('#comment-block-'+commentId).html('<div class="alert alert-dismissible alert-warning"><button type="button" class="close" data-dismiss="alert">&times;</button>Comment successfully deleted.</div>');
			$('#delete-comment-modal').modal('hide');
			//mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
}

mf.appendPostEvents = function() {
	
	$('#new-post-form').unbind();
	$("#new-post-form").submit(function(e) {
		var data = $("#new-post-form").serialize();		// uid, body
		var url = "/microfeed/posts/new";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var args = json;  //postId, uid, username, userImage, body
			var result = mf.templateEngine('post-template', args);
			$('#output').prepend(result);
			mf.appendEvents();
			$("#new-post-form textarea[name=body]").val('');
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$('.edit-post-btn').unbind();
	$('.edit-post-btn').click(function(e) {
		var postId = $(this).attr('data-post-id');
		$('#post-'+postId).hide();
		$('#edit-post-'+postId).show();
		e.preventDefault();
	});
	
	$('.delete-post-btn').unbind();
	$('.delete-post-btn').click(function(e) {
		var postId = $(this).attr('data-post-id');
		$('#delete-post-id').val(postId);
		$('#delete-post-modal').modal('show');
		e.preventDefault();
	});
	
	$('.cancel-edit-post').unbind();
	$('.cancel-edit-post').click(function() {
		var postId = $(this).attr('data-post-id');
		$('#edit-post-'+postId).hide();
		$('#post-'+postId).show();
	});
	
	$(".edit-post-form").unbind();
	$(".edit-post-form").submit(function(e) {
		var postId = $(this).attr('data-post-id');
		var data = $("#edit-post-form-"+postId).serialize();		// post_id, body
		var url = "/microfeed/posts/edit";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var postId = json.postId;
			$('#post-body-'+postId).html(json.body);
			$('#edit-post-'+postId).hide();
			$('#post-'+postId).show();
			mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
	
	$("#delete-post-form").unbind();
	$("#delete-post-form").submit(function(e) {
		var data = $('#delete-post-form').serialize();		// post_id, body
		var url = "/microfeed/posts/delete";
		$.ajax({
			url: url,
			data: data,
			type: "POST",
			dataType : "json"
		}).done(function( json ) {
			var postId = json.postId;
			$('#post-block-'+postId).replaceWith('<div class="alert alert-dismissible alert-warning"><button type="button" class="close" data-dismiss="alert">&times;</button>Post successfully deleted.</div>');
			$('#delete-post-modal').modal('hide');
			//mf.appendEvents();
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});

}

////////////////////////////////////////////

mf.loadPosts = function() {
	var data = {
		uid: 1
	}
	var url = "/microfeed/posts";
	$.ajax({
		url: url,
		data: data,
		type: "GET",
		dataType : "json"
	}).done(function( json ) {
		for (var i=0; i<json.length; i++) {
			var args = json[i];  //postId, uid, username, userImage, body
			var result = mf.templateEngine('post-template', args);
			$('#output').append(result);
			for (var j=0; j<json[i].comments.length; j++) {
				//alert(json[i].comments[j].body);
				var args2 = json[i].comments[j];
				var result2 = mf.templateEngine('comment-template', args2);
				//alert(result2);
				$('#comments-'+json[i].postId).append(result2);
			}
		}
		mf.appendEvents();
	}).fail(function( xhr, status, errorThrown ) {
		$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
		console.log( "Error: " + errorThrown );
		console.log( "Status: " + status );
		console.dir( xhr );
	});
}


////////////////////////////////////////////////

$( document ).ready(function() {
	
	mf.loadPosts();

});















