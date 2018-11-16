<template>
  <v-app>
    <v-navigation-drawer
      persistent
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >

      <user-card></user-card>
      <v-list>
        <v-list-tile
          value="true"
          v-for="(item, i) in items"
          :key="i"
          :to="{path: item.link}"
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      app
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-spacer></v-spacer>
      <v-toolbar-title> G2G Control Panel</v-toolbar-title><v-spacer></v-spacer><v-icon>pan_tool</v-icon>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>

    <v-footer :fixed="true" app>
      <span>CE KMITL&copy; 2018</span>
    </v-footer>
  </v-app>
</template>

<script>
import UserCard from './components/UserCard.vue'
export default {
  data () {
    return {
      drawer: true,
      items: [{
        icon: 'accessibility',
        title: 'Gestures',
        link: '/gestures'
      }, {
        icon: 'supervised_user_circle',
        title: 'Live Data Visualization',
        link: '/allimu'
      }]
    }
  },
  components: {
    UserCard
  },
  name: 'App'
}
</script>

<style>
img {
  width: 100%;
  height: 100%;
}
</style>
