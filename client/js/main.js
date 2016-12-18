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
    .when("/add", {
        templateUrl: "create_post.html",
        controller: "CreatePostController"
        //templateUrl: "show_post.html",
        //controller: "ShowPostController"
    })
    .otherwise({
        redirectTo: '/'
    });
});

app.controller("PostListController", function ($scope, $http) {
    console.log("Get List:Start");
    $http.get("http://localhost:5000/api/v1.0/posts")
    .then(function (response) {
        console.log("Get List:Succuess");
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

app.controller("CreatePostController", function ($scope, $http) {
    console.log("CreatePostController");
    //$http.post("http://localhost:5000/api/v1.p/")
});
