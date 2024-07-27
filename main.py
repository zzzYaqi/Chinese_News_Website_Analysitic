import flask_demo


def main():
    flask_demo.app.run(debug=True)


if __name__ == '__main__':
    # schedule.every().day.at("00:01").do(main())
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
