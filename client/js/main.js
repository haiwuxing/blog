var app = angular.module("blogApp", ["ngRoute"]);

app.config(function ($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl: "post_list.html",
        controller: 'PostListController'
    })
    .when("/show_post/:post_id", {
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

app.controller("ShowPostController", function ($scope, $http, $routeParams) {
    post_id = $routeParams.post_id;
    rest_url = "http://localhost:5000/api/v1.0/posts/" + post_id;
    $http.get(rest_url)
    .then(function (response) {
        $scope.post = response.data.post;
        console.log(response);
    });
});
