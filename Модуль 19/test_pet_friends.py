from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='Мурзик', animal_type='Кот', age='6'):
    """ Проверяем возможность добавления питомца (без фото) с корректными данными """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_add_photo_of_pet(pet_photo="images/11.jpg"):
    """ Проверяем возможность добавления фото к информации о своем питомце """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result["pet_photo"]
    else:
        raise Exception("No pets")


def test_get_api_key_for_data_user_empty(email=empty_email, password=empty_password):
    """ Проверяем что запрос api ключа c пустыми значениями логина и пароля возвращает статус 403
    и в результате не содержится слово key """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result


def test_get_api_key_for_password_user_empty(email=valid_email, password=empty_password):
    """ Проверяем что запрос api ключа c валидным значением логина и пустым значением пароля возвращает статус 403
    и в результате не содержится слово key """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result


def test_get_all_pets_with_empty_key(filter=""):
    """ Проверяем что запрос всех питомцев c пустым значением api ключа возвращает статус 403 """
    status, result = pf.get_list_of_pets(empty_auth_key, filter)
    assert status == 403


def test_get_all_pets_with_incorrect_key(filter=""):
    """ Проверяем что запрос всех питомцев c некорректным значением api ключа возвращает статус 403 """
    status, result = pf.get_list_of_pets(incorrect_auth_key, filter)
    assert status == 403


def test_add_new_pet_empty_data(name="", animal_type="", age="", pet_photo="images/1661443366_45.jpg"):
    """ Проверяем возможность добавить питомца с фото и незаполненными данными (это баг, так быть не должно)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name


def test_add_new_pet_incorrect_age(name="Шерхан", animal_type="Тигр", age="-1", pet_photo="images/1661443366_45.jpg"):
    """ Проверяем возможность добавить питомца с отрицательным возрастом (это баг, так быть не должно) """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["age"] == age


def test_delete_not_your_pet():
    """ Проверяем возможность удаления не своего питомца (это баг, так быть не должно) """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    if len(all_pets["pets"]) > 0:
        pet_id = all_pets["pets"][0]["id"]
        status = pf.delete_pet(auth_key, pet_id)
        assert status != 200
        assert pet_id not in all_pets.values()
    else:
        raise Exception("No pets")


def test_update_not_your_pet_info(name="Балу", animal_type="Медведь", age="15"):
    """ Проверяем возможность обновления информации не о своем питомце (это баг, так быть не должно) """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    if len(all_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, all_pets["pets"][0]["id"], name, animal_type, age)
        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("No pets")


def test_add_new_pet_without_photo_empty_data(name="", animal_type="", age=""):
    """ Проверяем возможность добавления питомца (без фото) с незаполненными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_set_photo_not_your_pet(pet_photo="images/Linda.jpg"):
    """ Проверяем возможность добавления фото к информации не о своем питомце """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    if len(all_pets["pets"]) > 0:
        pet_id = all_pets["pets"][0]["id"]
        status, result = pf.set_photo_pet(auth_key, pet_id, pet_photo)
        assert status == 500
    else:
        raise Exception("No pets")
