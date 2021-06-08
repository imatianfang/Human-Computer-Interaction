// 初始化喜爱列表,id=0不可被删除
var favorite_list = [
    {
        id:0,
        src:"favorites/favorite0.jpg"
    },
    {
        id:0,
        src:"favorites/favorite1.jpg"
    },
    {
        id:0,
        src:"favorites/favorite2.jpg"
    }
];

localStorage.setItem(-1, "likeImg");
localStorage.setItem(0, "likeImg");
localStorage.setItem(1, "likeImg");

const favorite_img_num = 3;

Array.prototype.remove = function (val) {
    for (var i = 0; i < this.length; ++i) {
        if (val == this[i].id) {
            this.splice(i,1)
            return i;
        }
    }
    return -1;
}

function updateFavoriteList() {
    // 显示在轮播图中
    for (var i = 0; i < favorite_img_num; ++i) {
        document.getElementById("favImg" + i).src = favorite_list[favorite_list.length - i - 1].src;
    }
}

function onClickImgLike(obj) {
    const btnId = obj.id.substr(-1);

    const img = document.getElementById("img" + btnId);
    const index = img.src.lastIndexOf('m') + 1;
    const imgId = img.src.substr(index).split('.')[0];
    // console.log(imgId)

    if (localStorage.getItem(imgId) == "likeImg") {
        // 已经在喜欢列表中，取消喜欢
        //console.log("dislike")

        localStorage.removeItem(imgId)
        favorite_list.remove(imgId)

        // 修改界面
        document.getElementById("likeImg"+String(btnId)+"-icon").className="glyphicon glyphicon-star-empty";
        document.getElementById("likeImg"+String(btnId)+"-text").innerText = "收藏";
    }
    else {
        // 未在喜欢列表中，加入列表
        //console.log("like")

        localStorage.setItem(imgId, "likeImg");
        imgLike = {
            id: imgId,
            src: "result/im" + String(imgId) + ".jpg",
        }
        favorite_list.push(imgLike)
        // 修改界面显示
        iconId = "likeImg"+String(btnId)+"-icon";
        document.getElementById("likeImg"+String(btnId)+"-icon").className="glyphicon glyphicon-star";
        document.getElementById("likeImg"+String(btnId)+"-text").innerText = "已收藏";
    }
    updateFavoriteList();
}