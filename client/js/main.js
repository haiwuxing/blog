var app = angular.module("blogApp", ["ngRoute"]);

app.config(function ($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl: "post_list.html",
        controller: 'PostListController'
    })
    .when("/show_post", {
        templateUrl: "show_post.html",
        controller: "ShowPostController"
     })
    .otherwise({
        redirectTo: '/'
    });
});

app.controller("PostListController", function ($scope, $http) {
    $http.get("http://localhost:5000/api/v1.0/posts")
    .then(function (response) {
        //console.log("Success");
        $scope.posts = response.data.posts;
        //console.log(response);
    });
});

app.controller("ShowPostController", function ($scope, $http) {
    $http.get("http://localhost:5000/api/v1.0/posts/1")
    .then(function (response) {
        console.log("Success");
        $scope.post = response.data.post;
        console.log(response);
    });
});
