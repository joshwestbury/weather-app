#!/usr/bin/env python3
import os
import tornado.ioloop
import tornado.web
import tornado.log
import json

import requests

from jinja2 import \
    Environment, PackageLoader, select_autoescape

ENV = Environment(
    loader=PackageLoader('weather', 'templates'),
    autoescape=select_autoescape(['html', 'xml']))


class TemplateHandler(tornado.web.RequestHandler):
    def render_template(self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))


class MainHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("form.html", {})


class WeatherDisplay(TemplateHandler):
    # def get(self):
    #     self.set_header('Cache-Control',
    #                     'no-store, no-cache, must-revalidate, max-age=0')
    #     self.render_template("weather-results.html", data)

    def post(self):
        city = self.get_body_argument('city')
        # print(city)
        url = "http://api.openweathermap.org/data/2.5/weather"

        querystring = {"APPID": "2b9465868a2cbea01eb629a79c177df3", "q": city}

        headers = {
            'authorization': "Basic Og==",
            'cache-control': "no-cache",
            'postman-token': "067b17ec-0564-a426-78a0-562598093b66"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)
        print(data)

        # render the weather data
        self.render_template("weather-results.html",
                             {'data': data,
                              'weather': data['weather']})


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/results", WeatherDisplay),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {
                'path': 'static'
            }),
        ],
        autoreload=True)


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(int(os.environ.get('PORT', '8080')))
    tornado.ioloop.IOLoop.current().start()
