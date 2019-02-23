<template>

  <v-card>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">User</h3>
          </div>
        </v-card-title>

        <v-select
          v-model="currentProfileName"
          :items="getProfileList"
          box
          label="Profiles"
        ></v-select>

        <v-card-actions>
          <v-layout column>
            <v-flex><v-btn outline block color="primary"  @click='createProfile'>+ Create new profile</v-btn></v-flex>
            <v-flex v-if='getCurrentProfile.name !== "Default"'><v-btn flat block color="red" @click='deleteProfile'>- Delete profile</v-btn></v-flex>
          </v-layout>
        </v-card-actions>
      </v-card>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  data () {
    return {

    }
  },
  computed: {
    ...mapGetters(['getProfileList', 'getCurrentProfile']),

    currentProfileName: {
      get: function () {
        return this.getCurrentProfile.name
      },
      set: function (newProfile) {
        this.CHANGE_PROFILE(newProfile)
      }
    }
  },
  methods: {
    ...mapMutations(['CHANGE_PROFILE', 'CREATE_PROFILE', 'DELETE_PROFILE']),
    createProfile () {
      let newname = prompt('Please enter profile name:', '')
      if (newname !== null && newname !== '') {
        this.CREATE_PROFILE(newname)
      }
    },
    deleteProfile () {
      if (confirm(`Are you sure you want to remove "${this.getCurrentProfile.name}" profile ?`)) {
        this.DELETE_PROFILE(this.getCurrentProfile.name)
      } else {
        // Do nothing!
      }
    }
  }
}
</script>

<style scoped>
img {
  width: 100%;
  height: 100%;
}
</style>
