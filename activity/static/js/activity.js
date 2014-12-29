function join_activity()
{
    $.getJSON(
		'/activity/join',
		{ activityid: $('#activityid').val() },
		function(data)
		{
			join_process(data);
		});
}

function join_process(data)
{
    if (data.status == 1) {
        var list_item = '<li id="participants' + data.id + '"> \
                            <div class="row list-item">\
                                <a href="/info/' + data.id + '">' + data.name + '</a>\
                            </div>\
                         </li>';
        $('#participants-list').prepend(list_item);
    }
}

function quit_activity()
{
    $.getJSON(
		'/activity/quit',
		{ activityid: $('#activityid').val() },
		function(data)
		{
			quit_process(data);
		});
}

function quit_process(data)
{
    if (data.status == 1) {
        $('#participants-list').children('#participants' + data.id).remove();
    }

}

function del_comment(data)
{
    $.getJSON(
		'/activity/del_comment',
		{ commentid: data },
		function(data)
		{
			del_comment_process(data);
		});
}

function del_comment_process(data)
{
    if (data.status == 1) {
        $('.activity-comment').children('#comment' + data.commentid).remove();
    }
}