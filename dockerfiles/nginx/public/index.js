/*if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/sw.js').then(() => {
            console.log('登録成功');
        }, () => {
            console.log('登録失敗');
        });
    });
}*/
var tagLang
fetch('/lang.json') // (1) リクエスト送信
    .then(response => response.json()) // (2) レスポンスデータを取得
    .then(data => { // (3)レスポンスデータを処理
        tagLang = data
        for (const element of Object.entries(data)) {
            // selectタグを取得する
            var select = document.getElementById("searchTags");
            // optionタグを作成する
            var option = document.createElement("option");
            // optionタグのテキストを4に設定する
            option.text = element[1];
            // selectタグの子要素にoptionタグを追加する
            select.appendChild(option);
        }
    });

class PostElement extends HTMLElement {
    #backgroundImageURL
    quizEndFunction
    #correctAnser=false
    constructor() {
        super();
        this.onclick =this.open
    }
    static get observedAttributes() {
        return ["data-post-ulid"];
    }
    async #getThumbnail(postULID) {
        var url = `/api/get?id=${postULID}&size=thumbnail`;

        var response
        
        if(typeof caches=="undefined"){
            response = await fetch(url).catch((e)=>{print("error",e)});
        }else{
            const cache = await caches.open("thumbnailCache");
            const cachedResponse = await cache.match(url);
            if (cachedResponse) {
                response = cachedResponse
            } else {
                response = await fetch(url);
                await cache.put(url, response.clone());
            }
        }


        const data = await response.blob()

        return data

    }
    async attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case "data-post-ulid":
                this.#backgroundImageURL=URL.createObjectURL(await this.#getThumbnail(newValue))
                this.style.backgroundImage = `url(${this.#backgroundImageURL})`
                break;
            default:
                break;
        }
    }
    inputQuizEndFunction(func){
        quizMode=true
        this.#correctAnser=true
        this.quizEndFunction=func
    }
    open(){
        if(quizMode&&this.#correctAnser){
            quizMode=false
            this.#correctAnser=false
            this.quizEndFunction()
            return
        }
        if(quizMode){
            return
        }
        location.href = `/api/get?id=${this.dataset.postUlid}`
        
    }
    disconnectedCallback() {
        URL.revokeObjectURL(this.#backgroundImageURL)
    }
}
customElements.define("post-element", PostElement)
var quizMode=false
class Quiz {
    #question
    #dateWhenQuizStart
    #quizElement = document.getElementById("quiz")
    #quizContentElement = document.getElementById("quizContent")
    #quizCountElement = document.getElementById("quizCount")
    #counting = false
    constructor() {
        this.#question = document.getElementsByTagName("post-element")[Math.floor(Math.random() * (document.getElementsByTagName("post-element").length + 1))].dataset.postUlid
        this.#quizContentElement.src = ""
        this.#quizContentElement.src = `/api/get?id=${this.#question}`
        this.#quizElementDisplay("show")
    }
    #quizElementDisplay(mode) {
        switch (mode) {
            case "hide":
                this.#quizElement.classList.remove("show")
                this.#quizElement.classList.remove("pinp")
                break;
            case "show":
                this.#quizElement.classList.add("show")
                this.#quizElement.classList.remove("pinp")
                break;
            case "pinp":
                this.#quizElement.classList.remove("show")
                this.#quizElement.classList.add("pinp")
                break
            default:
                break;
        }
    }
    countStart() {
        if (this.#counting) {
            return
        }
        this.#counting = true
        this.#quizElementDisplay("show")
        let count = 5
        let interval = setInterval(() => {
            this.#quizCountElement.innerText = count
            if (count <= 0) {
                clearInterval(interval)
                this.#quizStart()
                this.#counting = false
            }
            count--
        }, 1000);
    }
    cancel() {
        this.#quizElementDisplay("hide")
        this.#question = ""
    }
    #quizStart() {
        this.#quizElementDisplay("pinp")
        this.#dateWhenQuizStart = new Date();
        document.querySelector(`[data-post-ulid="${this.#question}"]`).inputQuizEndFunction(()=>{            
            this.#quizElementDisplay("hide")
            var time = new Date(new Date - this.#dateWhenQuizStart)
            alert(`正解! ${time.getMinutes()}分${time.getSeconds()}秒で正解しました。`)
        });
        quizMode=true
    }
    quizEnd() {
        this.#quizElementDisplay("hide")
        var time = new Date(this.#dateWhenQuizStart - new Date)
        alert(`正解! ${time.getMinutes()}分${time.getSeconds()}秒で正解しました。`)
    }
}

function startQuiz() {
    quiz = new Quiz()
    document.getElementById("quizStart").onclick = () => {
        quiz.countStart()
    }
}

function loadPosts(data) {
    data.sort((a, b) => {
        //a.takenAt-b.takenAt
        if (a.takenAt > b.takenAt) {
            return -1
        } else {
            return 1
        }
    })
    data.forEach((post, index) => {
        /*if(index>10){
            return
        }*/
        let postElement = document.createElement('post-element');
        postElement.dataset.postUlid = post.ULID
        //postElement.style.order=post.takenAt
        document.getElementById("seachResult").appendChild(postElement);
    })
}

fetch("/api/search")
    .then(response => response.json())
    .then(data => {
        //キャッシュ開放動作しないと…
        loadPosts(data)
    })

document.getElementById("searchWords").onchange = () => {

    /*for (const element of Object.entries(tagLang)) {
        if (document.getElementById("searchWords").value == element[1]) {
            tagID = Number(element[0]) + 1
            break
        }
    }*/
    var searchWords = document.getElementById("searchWords").value
    if (searchWords == "") {
        var path = "/api/search"
    } else {
        var tagID = Number(Object.keys(tagLang).find(key => tagLang[key] === searchWords)) + 1
        var path = `/api/search?s={"tag":[${tagID}]}`
    }

    fetch(path)
        .then(response => response.json())
        .then(data => {
            document.getElementById("seachResult").innerHTML = ""
            //なんの処理???
            if (data == null) {
                return
            }
            loadPosts(data)
        })
}

function light(){
    var i=0
    for (let element of document.getElementsByTagName("post-element")) {
        if(i>2){
            element.remove()
        }else{
            i++
        }
    }
}