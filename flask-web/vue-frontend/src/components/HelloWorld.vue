<template>
  <div>
    <div>
      <h1>Please upload query image here</h1>
      <input type="file" @change="onFileChange">
      <button @click="uploadImage">Upload</button>
      <p v-if="uploadStatus">{{ uploadStatus }}</p>
      <button @click="fetchData">Search</button>
      <p v-if="getDataResponse">{{ getDataResponse }}</p>
    </div>
    <div>
      <img alt="Received Image" :src="imageURL" v-if="imageURL">
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      uploadStatus: null,
      getDataResponse: null,
      bird_species: null,
      imageURL: null
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    uploadImage() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      axios.post('http://localhost:5001/upload', formData)
      .then(response => {
        this.uploadStatus = response.data.message;
        console.log(response.data);
      })
      .catch(error => {
          if (error.response) {
              console.error('Server responded with non-2xx code:', error.response.data);
          } else if (error.request) {
              console.error('No response received:', error.request);
          } else {
              console.error('Error setting up the request:', error.message);
          }
          console.error('Config:', error.config);
      });
    },
    fetchData() {
      axios.get('http://localhost:5001/get')
      .then(response => {
        this.getDataResponse = response.data;
        this.bird_species = this.getDataResponse["bird_species"];
        this.imageURL = this.getDataResponse['img_url'];
        console.log('bird_species', this.getDataResponse['bird_species']);
        console.log('img url:', this.getDataResponse['img_url']);
      })
      .catch(error => {
        console.error('GET request failed:', error);
      });
    }
  }
};
</script>
