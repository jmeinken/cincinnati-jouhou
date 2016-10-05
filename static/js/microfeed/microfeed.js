mf = {}


/// PARAMETERS ////////////////////////////////////////////////////////////////////////////////

mf.uid = 0;				//application needs to set this, otherwise nothing will be editable
mf.lastPostId = 0;

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
			//append comment options
			var commentUserOptionsStr = mf.templateEngine('comment-user-options-template', args);
			if (args.editable) {
				$('#comment-user-options-'+args.commentId).html(commentUserOptionsStr);
			}
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
	
	$('.show-hidden-comments').click(function(e) {
		postId = $(this).attr('data-post-id');
		$('#hidden-comments-block-'+postId).show();
		$(this).parent().remove();
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
			//append post options
			var postUserOptionsStr = mf.templateEngine('post-user-options-template', args);
			if (args.editable) {
				$('#post-user-options-'+args.postId).html(postUserOptionsStr);
			}
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
	
	$('#show-more-posts-btn').click(function() {
		mf.loadPosts();
	});

}

////////////////////////////////////////////

mf.loadPosts = function() {
	var data = {
		uid: mf.uid,
		last_post_id: mf.lastPostId,
		post_count: 10,
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
			//append post options
			var postUserOptionsStr = mf.templateEngine('post-user-options-template', args);
			if (json[i].editable) {
				$('#post-user-options-'+json[i].postId).html(postUserOptionsStr);
			}
			// append comments
			var commentCount = json[i].comments.length
			if (commentCount > 4) {
				var hiddenCommentBlock = mf.templateEngine('hidden-comments-template', args);
				//alert(result2);
				$('#comments-'+json[i].postId).append(hiddenCommentBlock);
				for (var j=0; j<commentCount; j++) {
					var args2 = json[i].comments[j];
					var result2 = mf.templateEngine('comment-template', args2);
					if (j < commentCount-3) {
						$('#hidden-comments-block-'+json[i].postId).append(result2);
					} else {
						$('#comments-'+json[i].postId).append(result2);
					}
					//append comment options
					var commentUserOptionsStr = mf.templateEngine('comment-user-options-template', args2);
					if (json[i].comments[j].editable) {
						$('#comment-user-options-'+json[i].comments[j].commentId).html(commentUserOptionsStr);
					}
				}
			} else {
				for (var j=0; j<commentCount; j++) {
					var args2 = json[i].comments[j];
					var result2 = mf.templateEngine('comment-template', args2);
					$('#comments-'+json[i].postId).append(result2);
					//append comment options
					var commentUserOptionsStr = mf.templateEngine('comment-user-options-template', args2);
					if (json[i].comments[j].editable) {
						$('#comment-user-options-'+json[i].comments[j].commentId).html(commentUserOptionsStr);
					}
				}
			}
		}
		$('#show-more-posts-block').remove();
		if (json.length == 10) {
			var result = mf.templateEngine('more-posts-template', args);
			$('#output').append(result);
			mf.lastPostId = json[9].postId;
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
	
	//load main container
	args = {
		uid: mf.uid
	}
	var result = mf.templateEngine('main-container-template', args);
	$('#microfeed-container').html(result);
	
	//load modals
	args = {}
	var result = mf.templateEngine('modals-template', args);
	$('#microfeed-modals').html(result);
		
	//load first set of posts
	mf.loadPosts();

});















