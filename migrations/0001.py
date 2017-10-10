import models


def forward():
    models.DB.create_tables([models.City])


if __name__ == '__main__':
    forward()
