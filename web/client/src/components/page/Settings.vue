<template>
  <v-container fluid grid-list-md>
    <v-layout column justify-space-around>
      <v-flex>
        <v-card>
          <v-card-title primary-title><div class="headline">Network Settings</div></v-card-title>
          <v-card-text class="grey lighten-5">
            <v-layout column align-start justify-space-around>
              <v-flex>
                <h4>Mode</h4>
                <v-btn-toggle v-model="mode">
                  <v-btn flat value='AP'>
                    <v-icon>wifi_tethering</v-icon>AP
                  </v-btn>
                  <v-btn flat value='Station'>
                    <v-icon>network_wifi</v-icon>Station
                  </v-btn>
                </v-btn-toggle>
              </v-flex>
              <v-flex v-if="mode!=='AP'">
                <h4>Wifi info</h4>
                <v-text-field label="Wifi Name" v-model="wifiName" ref='wifiNameField' :rules="nameRules"></v-text-field>
                <v-text-field label="Wifi Password" v-model="wifiPw" ref='wifiPwField' :rules="pwRules"></v-text-field>
                <v-btn v-for="(v,i) in getConnection" :key=i @click="saveNw(v)">{{v}}</v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-actions>
            <v-btn color='green'  @click='saveNw()'>Apply</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import {mapGetters, mapMutations, mapActions} from 'vuex'
export default {
  data () {
    return {
      mode: 'AP', // AP, Station
      wifiName: '@Glove2Gesture is here!',
      wifiPw: '12345678',
      nameRules: [v => !!v || 'Name is required'],
      pwRules: [v => v.length >= 8 || 'Password must contain 8 or more characters, now: ' + v.length]
    }
  },
  computed: {
    ...mapGetters(['getConnection'])
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    saveNw (name = this.wifiName) {
      if (this.mode === 'AP') {
        let r = confirm(`Disconnect from network and open the access point?`)
        if (r === true) {
          this.$socket.emit('openAP')
        }
      } else {
        let r = confirm(`Connect to '${name}' network?`)
        if (r === true) {
          this.$socket.emit('switchNw', name, this.wifiPw)
        }
      }
    }

  },
  watch: {

  },
  mounted () {
    this.$socket.emit('getNw')
  },
  components: {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
