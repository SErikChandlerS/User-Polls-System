<template>
  <v-card class="mx-auto">
    <v-row>
      <v-col v-for="(item, i) in candidates" :key="i" cols="10" style="margin: 2%">
        <v-card :color="white" light>
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="headline" v-text="item.name"></v-card-title>
              <v-card-subtitle style="color:black">Votes: {{ item.votes }}</v-card-subtitle>
              <v-card-subtitle>
                <v-expansion-panels v-model="panel" :disabled="disabled">
                  <v-expansion-panel>
                    <v-expansion-panel-header>Details</v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <b>Frontend skills:</b> {{ item.frontend }}
                      <br />
                      <b>Backend skills:</b> {{ item.backend }}
                      <br />
                      <b>Fullstack skills:</b> {{ item.fullstack }}
                      <br />
                      <b>Devops skills:</b> {{ item.devOps }}
                      <br />

                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-card-subtitle>
              <v-card-actions>
                <v-btn class="btn-success" style="color:white" text v-on:click="vote(item)">Vote</v-btn>
              </v-card-actions>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      candidates: [],
    };
  },
  created() {
    console.log("Here");
    this.all();
  },
  methods: {
    vote: function (candidate) {
      if (confirm("Vote " + candidate.name)) {
        axios
          .post(`http://localhost:8000/api/vote/`, {
            candidate_name: candidate.name,
          })
          .then((response) => {
            console.log(response);
            alert("Voted for " + candidate.name)
            this.all()
          })
          .catch(function (error) {
            if (error.response) {
              console.log(error);
              alert("You are only allowed to vote once");
            }
          });
      }
    },
    all: function () {
      console.log("Getting data");
      axios.get("http://localhost:8000/api/candidate/", {
        auth: {
          username: "admin",
          password: "111qaw333"
        }
      }).then((response) => {
        this.candidates = response.data;
        console.log(response);
      });
    },
  },
};
</script>
