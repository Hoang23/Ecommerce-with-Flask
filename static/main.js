function switchTitleColour() {
    document.getElementsByClassName("second").style.color = "black";
}

function MyFunction(game) {    
    var leagueText = "<a href='https://twitter.com'>player1</a> <br> <a href='https://twitter.com'>player2</a> <br> <a href='https://twitter.com'>player3</a> <br> <a href='https://twitter.com'>player4</a> <br> <a href='https://twitter.com'>player5</a>"
    var csgoText = "<a href='https://twitter.com'>player1</a> <br> <a href='https://twitter.com'>player2</a> <br> <a href='https://twitter.com'>player3</a> <br> <a href='https://twitter.com'>player4</a> <br> <a href='https://twitter.com'>player5</a>"
    var smashText = "<a href='https://twitter.com'>player1</a> <br> <a href='https://twitter.com'>player2</a>"
    var hsText = "<a href='https://twitter.com'>player1</a>"
    
    if(game == 'lol') {
        document.getElementsByClassName('lol-text')[0].innerHTML = leagueText;
    }
    if(game == 'cs') {
            document.getElementsByClassName('cs-text')[0].innerHTML = csgoText;
    } 
    if(game == 'smash') {
        document.getElementsByClassName('smash-text')[0].innerHTML = smashText;
    }  
    if(game == 'hs') {
        document.getElementsByClassName('hs-text')[0].innerHTML = hsText;
    } 
}



// function changeBackground()
//     var video = document.getElementsByTagName('video')[0];
//     video.onended = function(e) {
//     /*Do things here!*/
//     };

// function firstImage() {
//     var images = [{{product.Image_1}}, {{product.Image_2}}]
//     print(images)
//     }
    



