<template>
  <v-app>
    <v-navigation-drawer
      persistent
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >
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
export default {
  data () {
    return {
      drawer: true,
      items: [{
        icon: 'bubble_chart',
        title: 'Live Data Visualization',
        link: '/'
      }, {
        icon: 'bubble_chart',
        title: 'Predict',
        link: '/predict'
      }, {
        icon: 'bubble_chart',
        title: 'All IMU (Experiment)',
        link: '/allimu'
      }]
    }
  },
  name: 'App'
}
</script>
