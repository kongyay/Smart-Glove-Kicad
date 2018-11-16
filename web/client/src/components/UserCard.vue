<template>

  <v-card>
        <img
          src="@/assets/user.png"
          aspect-ratio="2.75"
        />

        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">User</h3>
          </div>
        </v-card-title>

        <v-select
          :items="getProfiles"
          box
          label="Profiles"
        ></v-select>

        <v-card-actions>
          <v-btn flat color="red">Logout</v-btn>
        </v-card-actions>
      </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data () {
    return {

    }
  },
  computed: {
    ...mapGetters(['getProfiles'])
  }
}
</script>

<style scoped>
img {
  width: 100%;
  height: 100%;
}
</style>
