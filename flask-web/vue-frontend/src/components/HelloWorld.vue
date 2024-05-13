<template>
  <div class="container">
    <h1>Please upload query image here</h1>
    <div>
      <input type="file" multiple @change="onFileChange">
      <button class="button upload-button" @click="uploadImage">Upload</button>
      <button class="button search-button" @click="fetchData">Search</button>
    </div>
    <p v-if="uploadStatus" class="status-message">{{ uploadStatus }}</p>
    <p v-if="getDataResponse" class="status-message">{{ getDataResponse }}</p>
    <p v-if="isloading">Searching similar images...</p> 
    <div v-if="imageURL" class="image-preview">
      <img alt="Received Image" :src="imageURL">
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: null,
      uploadStatus: null,
      getDataResponse: null,
      bird_species: null,
      imageURL: null,
      isloading: false
    };
  },
  created() {
    this.cleanupOnReload();
  },
  methods: {
    onFileChange(e) {
      this.selectedFiles = e.target.files;
    },
    uploadImage() {
      const formData = new FormData();
      Array.from(this.selectedFiles).forEach((file) => {
      formData.append('file[]', file); // Append each file under the same name 'file[]'
      });

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
      this.isloading = true
      axios.get('http://localhost:5001/get')
      .then(response => {
        this.getDataResponse = response.data;
        this.bird_species = this.getDataResponse["bird_species"];
        this.imageURL = this.getDataResponse['img_url'];
        console.log('bird_species', this.getDataResponse['bird_species']);
        console.log('img url:', this.getDataResponse['img_url']);
        this.isloading = false; 
      })
      .catch(error => {
        console.error('GET request failed:', error);
        this.isloading = false; 
      });
    },
    cleanupOnReload() {
    axios.post('http://localhost:5001/delete-uploads')
      .then(response => {
        console.log(response.data.message);  // Log success message
      })
      .catch(error => {
        console.error('Failed to clean up files:', error);
      });
    },
  }
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 20px;
}

.button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 12px 24px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #45a049;
}

.upload-button {
  background-color: #04536d; /* Blue */
}

.upload-button:hover {
  background-color: #007BAA;
}

.search-button {
  background-color: #f44336; /* Red */
}

.search-button:hover {
  background-color: #e33125;
}

.image-preview img {
  max-width: 100%;
  height: auto;
}
.status-message {
  color: #333; /* Or any color that fits your design */
  margin-top: 8px;
}

</style>