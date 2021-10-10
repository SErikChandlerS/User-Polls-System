import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      redirect: '/index'
    },
    {
      path: "/register",
      name: "register",
      component: () => import("./components/Register.vue")
    },
    /*{
      path: "/update/:id",
      name: "update",
      component: () => import("./components/Update.vue")
    },*/
    {
      path: "/index",
      name: "index",
      component: () => import("./components/Index.vue")
    },
  ]
});
