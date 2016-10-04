mf = {}

/// UTILITIES /////////////////////////////////////////////////////////////////////////////////

mf.templateEngine = function (templateId, args) {
	args = args || {};
	var template = $('#'+templateId).html();
	console.log(templateId);
	for (arg in args) {
		var str = '%' + arg + '%'
		template = template.split(str).join(args[arg]);
	}
	return template;
}


/// EVENTS /////////////////////////////////////////////////////////////////////////////////////

mf.appendEvents = function() {
	mf.appendNewPostEvents();
	mf.appendNewCommentEvents();
}

mf.appendNewCommentEvents = function() {
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
		}).fail(function( xhr, status, errorThrown ) {
			$('#search_status').html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>');
			console.log( "Error: " + errorThrown );
			console.log( "Status: " + status );
			console.dir( xhr );
		});

		e.preventDefault();
	});
}

mf.appendNewPostEvents = function() {
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















