package main

import (
	"gagger/crawler"
	irisadapter "gagger/adapter"
	"os"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/kataras/iris/v12"
	"log"
)

var irisLambda *irisadapter.irisadapter

func init() {
	app := iris.New()

	app.Get("/", func(ctx iris.Context) {
		ctx.JSON(crawler.Getter())
	})

	app.Get("/spec/{website}", func(ctx iris.Context) {
		website := ctx.Params().Get("website")
		ctx.JSON(crawler.Compiler(website))
	})

	app.Get("/about", func(ctx iris.Context) {
		ctx.JSON(iris.Map{
			"about": "just a simple web api"
		})
	})

	irisLamda = irisadapter.New(app)
	// config := atreugo.Config{
	// 	Addr: ":" + os.Getenv("PORT"),
	// }
	// server := atreugo.New(config)

	// server.GET("/", func(ctx *atreugo.RequestCtx) error {
	// 	// return ctx.TextResponse(strings.Join(crawler.MemeDroid(), " "))
	// 	return ctx.JSONResponse(crawler.Getter())
	// })

	// server.GET("/spec/{website}", func(ctx *atreugo.RequestCtx) error {
	// 	website := ctx.UserValue("website").(string)
	// 	return ctx.JSONResponse(crawler.Compiler(website))
	// })

	// server.GET("/about", func(ctx *atreugo.RequestCtx) error {
	// 	return ctx.JSONResponse(atreugo.JSON{"about": "just a simple web api"})
	// })

	// if err := server.ListenAndServe(); err != nil {
	// 	panic(err)
	// }
}

func Handler(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	// If no name is provided in the HTTP request body, throw an error
	return irisLambda.ProxyWithContext(ctx, req)
}

func main() {
	lambda.Start(Handler)
}
