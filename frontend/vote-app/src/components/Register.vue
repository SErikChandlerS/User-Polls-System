<template>
  <v-container>
    <v-form @submit="create" ref="form" lazy-validation>
      <v-text-field v-model="admin_id" :counter="250" label="Admin Id" required></v-text-field>
      <v-text-field v-model="admin_password" label="Admin Password" type="password" required></v-text-field>
      <v-text-field v-model="candidate.name" :counter="250" label="Name" required></v-text-field>
      <v-select
        v-model="candidate.frontend"
        :items="ratings"
        :rules="[v => !!v || 'Frontend skills rate is required']"
        label="Frontend Rating"
        required
      ></v-select>
      <v-select
        v-model="candidate.backend"
        :items="ratings"
        :rules="[v => !!v || 'Backend skills rate is required']"
        label="Backend Rating"
        required
      ></v-select>
      <v-select
        v-model="candidate.fullstack"
        :items="ratings"
        :rules="[v => !!v || 'Fullstack skills rate is required']"
        label="Fullstack Rating"
        required
      ></v-select>
      <v-select
        v-model="candidate.devOps"
        :items="ratings"
        :rules="[v => !!v || 'Devops skills rate is required']"
        label="Devops Rating"
        required
      ></v-select>
      <v-btn color="primary" type="submit">Submit</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      ratings: [1, 2, 3, 4, 5],
      num: 1,
      candidate: {
        name: "",
        frontend: 1,
        backend: 1,
        fullstack: 1,
        devOps: 1,
      },
      admin_id: "",
      admin_password: "",
      submitted: false,
    };
  },
  methods: {
    create: function () {
      axios
        .post("http://127.0.0.1:8000/api/candidate/", this.candidate, {
          auth: {
            username: this.admin_id,
            password: this.admin_password,
          },
        })
        .then((response) => {
          console.log(response);
          alert("Registered Succesfuly");
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
