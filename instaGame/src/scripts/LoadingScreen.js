import DarkIcon from '@/assets/instaGame-dark.svg';

function LoadingScreen(text) {
    //init the loader
  }
  LoadingScreen.prototype.displayLoadingUI = function() {
    if (document.getElementById("loadingScreenDiv")) {
        document.getElementById("loadingScreenDiv").style.display = "initial";
        return;
    }
    console.log("displayLoadingUI");
    this._loadingDiv = document.createElement("div");
    this._loadingIcon = document.createElement("img");
    this._loadingIcon.src = DarkIcon;
    this._loadingIcon.alt = "Loading";
    this._loadingIcon.id = "loadingIcon";
    this._loadingDiv.id = "loadingScreenDiv";
    this._loadingDiv.innerHTML = "Loading...";
    this.customLoadingScreenCss = `
      #loadingScreenDiv {
        position: absolute;
        width: 88%;
        height: 81%;
        text-align: center;
        font-size: 50px;
        background-color: black;
        z-index: 9999;
      }
      #loadingIcon {
        padding-top: 5%;
        width: 60%;
        height: 60%;
      }
    `;
    document.querySelector('style').textContent += this.customLoadingScreenCss;
    document.getElementById("gameContainer").appendChild(this._loadingDiv);
    document.getElementById("loadingScreenDiv").appendChild(document.createElement("p"));
    document.getElementById("loadingScreenDiv").appendChild(this._loadingIcon);
  };
  LoadingScreen.prototype.hideLoadingUI = function() {
			setTimeout(function(){
        document.getElementById("loadingScreenDiv").style.display = "none";
			}, 3000);
  };

  export default LoadingScreen;