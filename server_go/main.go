package main

import (
	"fmt"
	"strconv"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var Db *gorm.DB
var strs = [5]string{
	"on_off",
	"mode",
	"temp",
	"speed",
	"pref",
}

type go_air_set struct {
	ID        uint
	If_change int64 `json:"if_change"`
	On_off    int64 `json:"on_off"`
	Mode      int64 `json:"mode"`
	Temp      int64 `json:"temp"`
	Speed     int64 `json:"speed"`
	Pref      int64 `json:"pref"`
}

type api_post_airset_num struct {
	Num int `json:"num"`
}

type APIposttimeon struct {
	Time []APItimeonn `json:"time"`
}

type timeonn struct {
	ID uint
	APItimeonn
	Weekday int
}

type APItimeonn struct {
	// ID      uint
	H_start int
	M_start int
	H_end   int
	M_end   int
}

func init() {
	var err error
	sqlStr := "root:123456@tcp(81.68.216.118:3306)/MTTEST?charset=utf8mb4&parseTime=True&loc=Local"
	Db, err = gorm.Open(mysql.Open(sqlStr), &gorm.Config{})
	if err != nil {
		fmt.Println("err:", err)
	}
}

func main() {
	r := gin.Default()
	api := r.Group("/api")
	{
		get := api.Group("/get")
		{
			get.GET("/airset", func(ctx *gin.Context) {
				var fir go_air_set
				Db.Model(&go_air_set{}).First(&fir)
				ctx.JSON(200, gin.H{
					"ifchange": fir.If_change,
					"on_off":   fir.On_off,
					"temp":     fir.Temp,
					"mode":     fir.Mode,
					"speed":    fir.Speed,
					"pref":     fir.Pref,
				})
			})
			get.GET("/timeon/:ID", func(ctx *gin.Context) {
				ID := ctx.Param("ID")
				IDint, err := strconv.Atoi(ID)
				if err != nil {
					fmt.Println("can't convert to int")
				}
				var apitimeonns []APItimeonn
				result := Db.Model(&timeonn{}).Where(&timeonn{Weekday: IDint}).Find(&apitimeonns)
				fmt.Println(apitimeonns)
				ctx.JSON(200, gin.H{
					"time":   apitimeonns,
					"length": result.RowsAffected,
				},
				)
			})
			get.GET("/foresp32/airset", func(ctx *gin.Context) {
				var fir go_air_set
				Db.Model(&go_air_set{}).First(&fir)
				ctx.JSON(200, gin.H{
					"if_change": fir.If_change,
					"set": gin.H{
						"on_off":          fir.On_off,
						"needTemperature": fir.Temp,
						"Mode":            fir.Mode,
						"windSpeed":       fir.Speed,
						"personalMode":    fir.Pref,
					},
				})
				fir.If_change = 0
				Db.Save(&fir)
			})
			get.POST("/foresp32/airset", func(ctx *gin.Context) {
				var fir go_air_set
				Db.Model(&go_air_set{}).First(&fir)
				ctx.JSON(200, gin.H{
					"if_change": fir.If_change,
					"set": gin.H{
						"on_off":          fir.On_off,
						"needTemperature": fir.Temp,
						"Mode":            fir.Mode,
						"windSpeed":       fir.Speed,
						"personalMode":    fir.Pref,
					},
				})
				fir.If_change = 0
				Db.Save(&fir)
			})
		}
		post := api.Group("/post")
		{
			air_set := post.Group("/airset")
			{
				air_set.POST("/temp", func(ctx *gin.Context) {
					var numm api_post_airset_num
					ctx.ShouldBind(&numm)
					fmt.Println(numm.Num)
					var fir go_air_set
					Db.Model(&go_air_set{}).First(&fir)
					fir.Temp = int64(numm.Num)
					fir.If_change = 1
					Db.Save(&fir)
					ctx.JSON(200, gin.H{
						"temp": numm.Num,
					})
				})
				air_set.POST("/onoff", func(ctx *gin.Context) {
					var numm api_post_airset_num
					ctx.ShouldBind(&numm)
					fmt.Println(numm.Num)
					var fir go_air_set
					Db.Model(&go_air_set{}).First(&fir)
					fir.On_off = int64(numm.Num)
					fir.If_change = 1
					Db.Save(&fir)
					ctx.JSON(200, gin.H{
						"onoff": numm.Num,
					})
				})
				air_set.POST("/mode", func(ctx *gin.Context) {
					var numm api_post_airset_num
					ctx.ShouldBind(&numm)
					fmt.Println(numm.Num)
					var fir go_air_set
					Db.Model(&go_air_set{}).First(&fir)
					fir.Mode = int64(numm.Num)
					fir.If_change = 1
					Db.Save(&fir)
					ctx.JSON(200, gin.H{
						"mode": numm.Num,
					})
				})
				air_set.POST("/pref", func(ctx *gin.Context) {
					var numm api_post_airset_num
					ctx.ShouldBind(&numm)
					fmt.Println(numm.Num)
					var fir go_air_set
					Db.Model(&go_air_set{}).First(&fir)
					fir.Pref = int64(numm.Num)
					fir.If_change = 1
					Db.Save(&fir)
					ctx.JSON(200, gin.H{
						"pref": numm.Num,
					})
				})
				air_set.POST("/speed", func(ctx *gin.Context) {
					var numm api_post_airset_num
					ctx.ShouldBind(&numm)
					fmt.Println(numm.Num)
					var fir go_air_set
					Db.Model(&go_air_set{}).First(&fir)
					fir.Speed = int64(numm.Num)
					fir.If_change = 1
					Db.Save(&fir)
					ctx.JSON(200, gin.H{
						"speed": numm.Num,
					})
				})
			}
			timeon := post.Group("/timeon")
			{
				timeon.POST("/add", func(ctx *gin.Context) {
					var timeonn_post timeonn
					if err := ctx.ShouldBind(&timeonn_post); err != nil {
						fmt.Println("bind error!")
					}
					fmt.Println(timeonn_post)
					Db.Create(&timeonn_post)
					ctx.JSON(200, gin.H{
						"condition": "success",
						"time":      timeonn_post,
					})
				})
				timeon.POST("/updateall/:ID", func(ctx *gin.Context) {
					ID := ctx.Param("ID")
					var timeonns []timeonn
					var apiposttimeon APIposttimeon
					ctx.ShouldBindJSON(&apiposttimeon)
					IDint, err := strconv.Atoi(ID)
					fmt.Println(IDint)
					fmt.Println(apiposttimeon)
					Db.Model(&timeonn{}).Where(&timeonn{Weekday: IDint}).Find(&timeonns)
					Db.Model(&timeonn{}).Delete(&timeonns)
					// fmt.Println(ctx.Get("time"))
					if err != nil {
						fmt.Println("can't convert to int")
					}
					for _, item := range apiposttimeon.Time {
						Db.Model(&timeonn{}).Create(&timeonn{Weekday: IDint, APItimeonn: item})
					}
					ctx.JSON(200, gin.H{
						"TIME": apiposttimeon,
					})
				})
				timeon.POST("/deleteall/:ID", func(ctx *gin.Context) {
					ID := ctx.Param("ID")
					IDint, err := strconv.Atoi(ID)
					if err != nil {
						fmt.Println("can't convert to int")
					}
					var timeonns []timeonn
					Db.Model(&timeonn{}).Where(&timeonn{Weekday: IDint}).Find(&timeonns)
					Db.Model(&timeonn{}).Delete(&timeonns)
					ctx.JSON(200, gin.H{
						"status": 200,
						"sucess": "delete",
					})
				})
			}
		}
	}
	r.Run(":9094")
}
