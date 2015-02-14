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

function post_comment()
{
    var text = $('#newcomment').val();
    if(text != '')
    {
        $.getJSON(
		'/activity/post_comment',
		{ comment: text,
          activityid: $('#activityid').val()
        },
		function(data)
		{
			post_comment_process(data);
		});
    }
}

function post_comment_process(data)
{
    if (data.status == 1)
    {
        var elem = '<div class="row activity-comment-item" id="comment'+data.commentid+'">\
                        <div class="col-lg-10">\
                            <div class="row">';
        if(data.is_staff)
        {
            elem += '<div class="col-lg-4 text-left">\
                        <button class="btn btn-xs btn-danger" onclick="del_comment(' + data.commentid + ')">Del</button>\
                     </div>';
        }
        elem += '<div class="col-lg-8 text-right pull-right">\
                                    <p>\
                                        <strong>\
                                            '+data.name+'\
                                        </strong> @ '+data.datetime+
                                    '</p>\
                                </div>\
                            </div>\
                            <div class="row activity-comment-content">\
                                <p>' + data.content + '\
                                </p>\
                            </div>\
                        </div>\
                        <div class="col-lg-2">\
                                    <div>Image</div>\
                        </div>\
                </div>';
        $('.activity-comment-add').after(elem);
    }
}

function change_status()
{
    $.getJSON(
		'/activity/change_status',
		{ activityid: $('#activityid').val() },
		function(data)
		{
			change_status_process(data);
		});
}

function change_status_process(data)
{
    if(data.status == 1)
    {
        if(data.activity_status == 1)
        {
            $('#btn_manage_activity').text('Publish');
            $('#text_activity_status').text('Discussing');
        }
        else if(data.activity_status == 2)
        {
            $('#btn_manage_activity').text('Finish');
            $('#text_activity_status').text('Published');
        }
        else
        {
            $('#btn_manage_activity').remove();
            $('#text_activity_status').text('Finished');
        }
    }
}

function delete_activity_confirm()
{
    if(confirm('确定要删除该活动？'))
    {
        $.getJSON(
		'/activity/del_activity',
		{ activityid: $('#activityid').val() },
		function(data)
		{
            if(data.status == 1)
            {
                if (!window.location.origin)
                {
                    window.location.origin = window.location.protocol + "//" + window.location.host;
                }
                var newurl = window.location.origin + '/'+ data.url;
                window.location.assign(newurl);
            }
		});
    }
}

function request_manage_participants()
{
     $.getJSON(
		'/activity/req_manage_participants',
		{ activityid: $('#activityid').val() },
		function(data)
		{
            manage_participants(data)
		});
}

function manage_participants(data)
{
    if(data.status == 1)
    {
        $('.footer').after(data.content);
        $('#myModal').modal({
            backdrop: 'static',
            keyboard: false
        });
    }
}

function add_participants()
{
	$('#unjoin option:selected').each(function(index, elem)
	{
        elem = $(elem);
        elem.appendTo($('#joined'));
        //elem.remove();
    });
}

function add_all_participants()
{
	$('#unjoin option').each(function(index, elem)
	{
		elem = $(elem);
		elem.appendTo($('#joined'));
		//elem.remove();
	});
}

function del_participants()
{
	$('#joined option:selected').each(function(index, elem)
	{
		elem = $(elem);
		elem.appendTo($('#unjoin'));
		//elem.remove();
	});
}

function del_all_participants()
{
	$('#joined option').each(function(index, elem)
	{
		elem = $(elem);
		elem.appendTo($('#unjoin'));
		//elem.remove();
	});
}

function clean_dlg()
{
    $('#myModal').modal('hide');
	$('#myModal').remove();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
}

function submit_participants()
{
	var plist = [];
	$('#joined option').each(function(index, elem)
	{
		plist.push($(elem).val());
	});

	$.getJSON(
		'/activity/manage_participants',
		{ activityid: $('#activityid').val(),
		  plist: plist
		},
		function(data)
		{
            refersh_participants(data);
		});
}

function refersh_participants(data)
{
    if(data.status == 1)
    {
        $('#participants-list').empty();
        var infolist = eval(data.plistinfo);
        $.each(infolist, function(index, item){
            var list_item = '<li id="participants' + item.pk + '"> \
                            <div class="row list-item">\
                                <a href="/info/' + item.pk + '">' + item.fields.cname + '</a>\
                            </div>\
                         </li>';
            $('#participants-list').append(list_item);
        });
        clean_dlg();
    }
}