/**
 * 弹出式提示框，默认1.5秒自动消失
 * @param message 提示信息
 * @param style 提示样式，有alert-success、alert-danger、alert-warning、alert-info
 * @param time 消失时间
 */
 var prompt = function (message, style, time)
 {
     style = (style === undefined) ? 'alert-success' : style;
     time = (time === undefined) ? 1500 : time;
     $('<div>')
         .appendTo('body')
         .addClass('alert ' + style)
         .html(message)
         .show()
         .delay(time)
         .fadeOut();
 };

 // 成功提示
var success_prompt = function(message, time)
{
    prompt(message, 'alert-success', time);
};

// 失败提示
var fail_prompt = function(message, time)
{
    prompt(message, 'alert-danger', time);
};

// 提醒
var warning_prompt = function(message, time)
{
    prompt(message, 'alert-warning', time);
};

// 信息提示
var info_prompt = function(message, time)
{
    prompt(message, 'alert-info', time);
};

function myFunction() {

    document.getElementById("predictedResult").innerHTML = "";

    $('#clear').hide();
}

function search() {


    $('#load').show();
    

    $("form").submit(function (evt) {
        //$('#loader-icon').show(); 

        evt.preventDefault();

        //$('#loader-icon').show();
        var formData = new FormData();//声明一个FormData对象
        formData.append('file', document.getElementById("file-1").files[0]);
        

        if(formData.get('file')==="undefined"){
            console.log("未选择图片");
            warning_prompt("请先选择图片再搜索！",1500);
            $('#load').hide();
            return;
        }
        window.location.hash="#"
        // 记录执行时间
        let start = new Date().getTime();

        $.ajax({
            url: 'imgUpload',
            type: 'POST',
            data: formData,
            //async: false,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,

            success: function (response) {
                $('#load').hide();
                $('#row1').show();
                //$('#clear').show();
                console.log(response);

                localStorage.setItem("tags", response.tags);
                localStorage.setItem("total_item",response.total_item);

                //document.getElementById("predictedResult").innerHTML= response;
                for (var i = 0; i < response.total_item; ++i) {
                    document.getElementById("img" + String(i)).src = response["image" + String(i)].url;
                    document.getElementById("img-tag-" + String(i)).innerText = response["image" + String(i)].tag;
                }

                $('#table').show();
                $('#clear').show();

                let end = new Date().getTime();
                document.getElementById("time-of-search-result").innerText = end - start;
                document.getElementById("num-of-search-result").innerHTML = response.total_item;
                $("#search-result-info-label").show();

                $("ul").find("li").remove();

                // 生成tag标签
                for (var i = 0; i < response.tags.length; ++i) {
                    selectValue = $("<li><a id='img-tag"+String(i)+"'class='img-tag'>" + response.tags[i] + "</a></li>");
                    $("#tag-sort-menu").append(selectValue);
                    $(".img-tag").attr("onclick","sort_by_tag(this);");
                }

                $("#tag-dropdown").show();
                
                window.location.hash="#search-result";
                

            }
        });
        return false;
    })
}

function reset(){

}

function sort_by_tag(obj) {
    const target_tag = obj.innerText;
    for(var i=0;i<localStorage.getItem("total_item");++i){
        if(document.getElementById("img-tag-"+String(i)).innerText===target_tag){
            $("#result-image-box"+String(i)).show();
        }
        else{
            $("#result-image-box"+String(i)).hide();
            //document.getElementById("result-image-box"+String(i)).hide();
        }
    }
    console.log(obj.innerText)
}