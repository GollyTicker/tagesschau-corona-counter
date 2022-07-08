<template>
  <div id="app">
    <p>This site is WORK IN PROGRESS!</p>
    <h1>
      When is Corona considered over?
      <span style="font-size: 0.35em">
        <br/>
        (at least in Germany, Europe)
      </span>
    </h1>

    <h3>
      How often was "Corona" mentioned in the Tagesschau 20 Uhr in the past "30 days"?
    </h3>

    <!-- these explanations can come into a closeable paragraph. -->
    <p>
      The pandemic has been strongly influencing and shaping the lives of many humans
      around the world for more than one year. <br/>
      With the recent developments in vaccines and our possibility to organise ourselves, <br/>
      we have the tools in our hands to make the pandemic a thing of the past
      <span style="font-size: 0.7em">(and hopefully also learn for the next pandemic)</span>.
    </p>
    <p>
      We can ask ourselves the following question: <br/>
      <em>How could we precisely define, that the pandemic is over?</em>
      <br/><br/>
      This can be achieved in many ways. <br/>
      One definition would be based on the average number
      of Covid-19 infections in a given period of time. <br/>
      Another definition would be based on the number of times this topic is mentioned in the news. <br/>
      This news based definition tries to estimate the
      level of <em>interest</em> and <em>concern</em> for the topic <br/>
      rather than the number of infected people.
    </p>
    <p>
      On this page, we pursue the latter news-based approach. <br/>
      One indicator, for when the pandemic is considered <em>done</em>, is <br>
      when a main news channel in a country does not regularly report any updates on it.
    </p>
    <p>
      For Germany, we can choose the
      <a href="https://www.tagesschau.de/sendung/tagesschau/">Tagesschau 20 Uhr</a>. <br/>
      They report at 20:00 every evening and they are by far the mostly viewed news source in Germany.<a
        href="https://www.digitalfernsehen.de/news/medien-news/maerkte/tagesschau-liegt-auch-2015-bei-den-zuschauern-vorn-425584/">[x]</a>
      <br>
      From this thought, one can say, that Corona is considered <em>over</em><br/>
      when this news channel reports rarely about Corona.
      <br/>
      To make this question executable by a computer, <br/>
      we can formulate the following question:
    </p>
    <h3>
      When will the time come, that the term <span id="term" v-on:keyup="this.answerQuestion" class="input"
                                                   role="textbox" contenteditable>Corona</span>
      <br>
      is mentioned at-most <span id="maximumOccurrence" v-on:keyup="this.answerQuestion" class="input" role="textbox"
                                 contenteditable>1</span>
      time(s)<br>
      in the <em>Tagesschau 20 Uhr</em> daily news summary<br>
      in the most recent <span id="n" v-on:keyup="this.answerQuestion" class="input" role="textbox"
                               contenteditable>30</span> days?
    </h3>
    <p>{{ answer }}</p>
    <!-- TODO: handling of various resolutions?

      todo: einleitung könnte kürzer sein
      todo: justified textarea

      todo: I could use Elm for a clean and reliable developer experience :)

      Also, in many ways, security and reliability is much easier with
      languages like Elm and Haskell - rather than their conventional counterparts (JS, Java).
    -->
  </div>
</template>

<script>
// eslint-disable-next-line
const _ = require("lodash");


const requestURL = (term, n) =>
    "https://"
    + location.hostname + "/tagesschau-counter/api/"
    + "sum/" + encodeURIComponent(term)
    + "?n=" + encodeURIComponent(n)
    + "&start=2021.05.01&end=2021.05.01";

const getN = () => document.getElementById("n").innerText;
const getTerm = () => document.getElementById("term").innerText;
const getMaximumOccurrence = () => document.getElementById("maximumOccurrence").innerText;

// eslint-disable-next-line
function executeRequest(n, term) {
  const url = requestURL(term, n);
  console.log("URL:", url);
  const request = new Request(url);
  return fetch(request)
      .then(response => {
            console.log("Response status: ", response.ok, response.status);
            if (response.ok && response.status < 400) {
              return response.json();
            } else {
              return Promise.reject("Error with request: " + response.statusText);
            }
          }
      )
      .catch(console.log);
}

export default {
  name: 'App',
  components: {},
  data() {
    return {
      answer: "-"
    }
  },
  methods: {
    answerQuestion() {
      console.log("answer question with:", getN(), getTerm(), getMaximumOccurrence());
      executeRequest(getN(), getTerm()).then(this.processResult)
    },
    processResult(responseJson) {
      console.log("Response: ", responseJson);
      this.answer = responseJson.result;
    }
  }
}
</script>

<style>
.input {
  background-color: #f5f2ec;
  font: 1.3em monospace;
}

.input:focus {
  background-color: #8cb6ff;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
