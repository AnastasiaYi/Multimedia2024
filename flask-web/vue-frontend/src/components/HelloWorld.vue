<template>
  <div class="container">
    <h1>Please upload query image here</h1>
    <div>
      <input type="file" multiple @change="onFileChange">
      <button class="button upload-button" @click="uploadImage">Upload</button>
      <button class="button search-button" @click="fetchData">Search</button>
      <button class="button refresh-button" @click="refreshPage">Refresh</button>
    </div>
    <p v-if="uploadStatus" class="status-message">{{ uploadStatus }}</p>
    <p v-if="isloading">Searching similar images...</p>
    <div class="image-preview" v-if="imageURLs.length">
      <div v-for="(url, index) in imageURLs" :key="index" class="image-container">
        <img :src="url" alt="Received Image">
        <p>{{ bird_species[index] }}</p>
      </div>
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
      bird_species: [],
      imageURLs: [],
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
    refreshPage() {
    console.log("refresh")
    window.location.reload(); // Reload the page
    
    },
    fetchData() {
      this.isloading = true;
      this.bird_species = [];  // Clear previous data
      this.imageURLs = [];     // Clear previous data
      axios.get('http://localhost:5001/get')
        .then(response => {
          for (let i = 1; i <= 3; i++) {
            this.bird_species.push((response.data[`bird_species_${i}`])[0]);
            this.imageURLs.push((response.data[`img_url_${i}`]));
          }
          this.isloading = false;
          console.log((response.data['bird_species_1'])[0])
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

.image-preview {
  text-align: center; /* Ensure contents are centered */
  margin-top: 10px; /* Space between search text and images */
}

.image-container {
  display: inline-block; /* Align images horizontally */
  margin-right: 10px; /* Space between image blocks */
  max-width: 350px; /* Set max width for image container */
  width: 100%; /* Ensure container takes full width */
  vertical-align: top; /* Align the top of the elements */
}

.image-container img {
  width: 100%; /* Make images fill their container */
  height: auto; /* Maintain aspect ratio */
  display: block; /* Remove any default margins or padding */
}

.image-container p {
  text-align: center; /* Center the species text below the image */
  margin-top: 5px; /* Small space between image and text */
  color: #333; /* Optional: color for the species name */
}
.refresh-button {
  background-color: #ff6347; /* Tomato */
}

.refresh-button:hover {
  background-color: #e5533b;
}




</style>