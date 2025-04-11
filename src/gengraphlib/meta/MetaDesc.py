from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Self


class MetaDescriptorBase(ABC):
    def __init__( self: Self, _host: object, desc_name: str | None ) -> None:
        print(f"MetaDescriptorBase__init__( owner:{type( _host )}, desc_name:{desc_name} )" )
        print(f"    host.__class__ = {_host.__class__}" )
        self._desc_name: str = desc_name
        self._host: object = _host
        self._host_class = _host.__class__
#        object.__dict__[desc_name] = self

    def __set_name__(self, owner, name):
        print(f"MetaDescriptorBase[{self._desc_name}]__set__( owner:{type(owner)} )" )
        self._desc_name = name

    def __set__(self, instance, value):
        print(f'MetaDescriptorBase[{self._desc_name}]__set__( instance: {type(instance)}, value[{type(value)}]: {value} )')

    def __delete__(self, instance):
        print(f'MetaDescriptorBase[{self._desc_name}]__set__( instance: {type(instance)} )')

    @abstractmethod
    def __get__(self, instance, owner):
        print(f'MetaDescriptorBase[{self._desc_name}]__set__( instance: {type(instance)}, owner:{type(owner)} )')

TrackedItemRec: type = tuple[str, str]

class TrackedItem:

        def __init__( self, *args, **kwargs ):
            self.id: str = ""
            self.val: str = ""

            match args:
                case _id, _val if len(args) > 1:
                    self.id = _id
                    self.val = _val

                case _:
                    match kwargs:
                        case rec if isinstance(rec, tuple):
                            self.id = rec[0]
                            self.val = rec[1]

class KeyRepo(MetaDescriptorBase):
    keyrepo_inst: Self | None = None
    host_cnt: int = 0
    items_dict: dict[str, TrackedItem] = {}

    def __init__( self: Self, host_obj: object ) -> None:
        KeyRepo.host_cnt += 1
        if KeyRepo.keyrepo_inst is None:
            KeyRepo.keyrepo_inst = self

        super().__init__( host_obj, "key_repo" )

    def __get__(self, instance, owner) -> Self:
        super().__set__(instance, owner)
        return KeyRepo.keyrepo_inst

class HostClass:

    def __init__( self: Self, host_name: str ):
        self._host_name: str = host_name
        self._repo: KeyRepo = KeyRepo(self)

    def get_repo( self: Self ) -> KeyRepo:
        return self._repo

    @property
    def keydefs( self ) -> Generator[(str, str), None, None ]:
        for ky, vl in self._repo.items_dict.items():
            yield ky, vl.val

    def get_keydef( self, key_id: str ) -> str | None:
        return self._repo.items_dict.get(key_id, None)

    def set_keydef( self, key_id: str, val_str: str ) -> None:
        if key_id not in self._repo.items_dict:
            self._repo.items_dict[key_id] = TrackedItem(key_id, val_str)
        else:
            self._repo.items_dict[key_id].val = val_str

    def __add__(self, other: tuple[str, str]):
        self.set_keydef(other[0], other[1])
        return self

    def add_keydef( self: Self, item: TrackedItem ) -> None:
        self._repo.items_dict[item.id] = item

    def filter( self: Self, _gen: Generator[TrackedItemRec, str, None ] | None ):
        pass

if __name__ == "__main__":

    range_int: int = 10
    #test: Generator[TrackedItemRec, str, None] = ( )

    #print(test)
    host = HostClass("test_host")
    #host.filter(test)

    host.add_keydef( TrackedItem( "a1", "a1-val" ) )
    host.add_keydef( TrackedItem( "a2", "a2-val" ) )
    host.add_keydef( TrackedItem( "a3", "a3-val" ) )

    host += ("a4", "a4-val")

    host += (
        ("b4", "b4-val"),
        ("b5", "b5-val"),
        ("b6", "b6-val"),
    )

    for key, val in host.keydefs:
        print(f"item: {key} = {val}")










